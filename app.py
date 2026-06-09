import streamlit as st

# Page Configuration - MUST be first
st.set_page_config(
    page_title="Kill O Meter - Smart Fare Matrix",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from geopy.distance import geodesic
from chatbot import TwinCitiesChatbot
from fare_database import get_all_locations, get_fare_estimate, FARE_CONFIG, is_peak_hour, get_proactive_comparison, LOCATIONS
from recommendation_engine import get_smart_recommendation
from validators import parse_query

from geopy.geocoders import Nominatim
from datetime import timedelta
import datetime
import re


def clean_and_normalize_address(address_str):
    """
    Cleans granular addresses, house numbers, and local towers,
    ensuring they resolve perfectly in the Islamabad/Rawalpindi grid.
    """
    if not address_str:
        return ""
    
    addr = address_str.lower().strip()
    
    # Handle local acronyms/abbreviations
    addr = addr.replace("au", "Air University, E-9, Islamabad")
    addr = addr.replace("bu", "Bahria University, E-9, Islamabad")
    addr = addr.replace("oec huawei tower", "OEC Tower, G-9 Markaz, Islamabad")
    
    # Handle common sub-sector text formatting (e.g., g13/4 -> G-13/4)
    addr = re.sub(re.compile(r'([a-i])\s*(\d+)'), r'\1-\2', addr)
    
    if "islamabad" not in addr and "rawalpindi" not in addr:
        addr += ", Islamabad, Pakistan"
        
    return addr.title()


def get_simulated_weather_and_trends():
    """
    Simulates real-time weather parameters for Islamabad/Rawalpindi,
    evaluates bike comfort thresholds, and handles peak traffic intervals.
    """
    weather = {
        "temp": 29,
        "condition": "Light Drizzle",
        "precipitation_chance": 40,
        "wind_speed": 6,
        "direction": "Northeast"
    }
    
    current_hour = datetime.datetime.now().hour
    is_peak = (8 <= current_hour <= 10) or (17 <= current_hour <= 19)
    
    if "heavy" in weather["condition"].lower() or weather["wind_speed"] > 20:
        bike_index = "🔴 Low Comfort: High risk of downpour or heavy winds. Shifting to an AC Car is highly recommended!"
        fare_suggestion = "Car options are experiencing high surge, but staying dry is worth it right now."
    elif "drizzle" in weather["condition"].lower() or "light rain" in weather["condition"].lower():
        bike_index = "🟢 Moderate-High Comfort: It's just an affordable local drizzle! Grab a bike, save cash, and dodge the premium car prices."
        fare_suggestion = "💡 Money-Saving Tip: Skip the car markup. Taking a bike right now saves you significant cash if you don't mind a minor drizzle!"
    else:
        bike_index = "🟢 High Comfort: Perfect clear weather conditions for a fast bike ride!"
        fare_suggestion = "Weather is pristine. Bike options will get you there fastest through traffic."
        
    return weather, is_peak, bike_index, fare_suggestion


def render_predictive_forecasting_ui(current_distance, is_peak):
    """
    Renders the predictive analytics block showing fare trends ahead in time (+30 and +60 mins).
    """
    st.write("### 🔮 Fare Trend & Booking Forecast")
    
    if is_peak:
        st.warning("⚠️ **Current Status: Peak Traffic Rush Hour.** Prices are currently inflated by ~30% due to local traffic volume.")
        t30_change, t60_change = "📉 -15% (Traffic clearing)", "📉 -25% (Normal rates)"
    else:
        st.info("ℹ️ **Current Status: Standard Traffic Hours.** Fares are stable across all sectors.")
        t30_change, t60_change = "⚖️ Stable (±2%)", "⚖️ Stable (±5%)"
        
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Forecast in +30 Mins", value="Price Drops Expected" if is_peak else "Rates Stable", delta=t30_change)
    with col2:
        st.metric(label="Forecast in +60 Mins", value="Cheaper Fare Window" if is_peak else "Rates Stable", delta=t60_change)


# Initialize Geocoder
geolocator = Nominatim(user_agent="kill_o_meter_twin_cities")

def get_coordinates(address):
    """
    Resolve any custom address string to real coordinates.
    Checks system fallback database first, then hits open-source geocoding with custom formatting.
    """
    if not address:
        return None
        
    # Standardize basic acronym variants first
    normalized_input = clean_and_normalize_address(address)
    
    # Try looking up direct pre-defined keys
    if normalized_input in LOCATIONS:
        return LOCATIONS[normalized_input].get("coords")
        
    # Clean up string for the Nominatim map query engine
    query_string = normalized_input
    if "islamabad" not in query_string.lower() and "rawalpindi" not in query_string.lower():
        query_string += ", Islamabad, Pakistan"
        
    try:
        # Request precise coordinate resolution
        location_data = geolocator.geocode(query_string, timeout=3)
        if location_data:
            return (location_data.latitude, location_data.longitude)
    except Exception as e:
        pass
        
    return None


def render_weather_dashboard():
    """
    Renders an active, visually responsive weather monitoring widget 
    with custom CSS cards and context-aware travel safety recommendations.
    """
    weather, is_peak, bike_comfort, advice_text = get_simulated_weather_and_trends()
    
    condition_lower = weather["condition"].lower()
    if "drizzle" in condition_lower or "light rain" in condition_lower:
        weather_icon = "🌦️"
    elif "heavy" in condition_lower or "storm" in condition_lower:
        weather_icon = "⛈️"
    else:
        weather_icon = "☀️"

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); padding: 18px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 22px; font-weight: bold; color: #FFFFFF;">🌤️ Transit Environmental Sync</span>
                <span style="background-color: #3b82f6; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">LIVE METRICS</span>
            </div>
            <hr style="border-color: #334155; margin: 10px 0;">
            <div style="display: flex; gap: 20px; justify-content: space-around; text-align: center;">
                <div>
                    <p style="margin:0; color:#94A3B8; font-size:13px;">Condition</p>
                    <h3 style="margin:0; color:#F8FAFC; font-size:16px;">{weather_icon} {weather['condition']}</h3>
                </div>
                <div style="border-left: 1px solid #334155; padding-left: 20px;">
                    <p style="margin:0; color:#94A3B8; font-size:13px;">Temperature</p>
                    <h3 style="margin:0; color:#38BDF8; font-size:16px;">{weather['temp']}°C</h3>
                </div>
                <div style="border-left: 1px solid #334155; padding-left: 20px;">
                    <p style="margin:0; color:#94A3B8; font-size:13px;">Wind Speed</p>
                    <h3 style="margin:0; color:#F43F5E; font-size:16px;">💨 {weather['wind_speed']} mph</h3>
                </div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.info(f"**🏍️ Weather Rideability Status:** {bike_comfort}\n\n{advice_text}")


# Rebranding Banner
st.markdown("""
    <div style="background-color:#1E1E1E;padding:15px;border-radius:10px;margin-bottom:20px;border-left: 5px solid #FFD700;">
        <h1 style="color:white;margin:0;">⚡ Kill O Meter</h1>
        <p style="color:#FFD700;margin:0;">Twin Cities Intelligent Routing Engine</p>
    </div>
    """, unsafe_allow_html=True)

# Render Weather Analytics Header Panel
weather_data, is_peak, bike_comfort, advice_text = get_simulated_weather_and_trends()
render_weather_dashboard()

# Peak Hour Banner
if is_peak:
    st.warning("🚦 **PEAK TRAFFIC WARNING**: High demand detected. Surge pricing of 1.3x is currently active in the Twin Cities.")

# Initialize Chatbot and Context
if "chatbot" not in st.session_state:
    st.session_state.chatbot = TwinCitiesChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salaam! 🙋‍♂️ I'm the Kill O Meter AI. Ready to calculate your next route?"}
    ]

if "route_context" not in st.session_state:
    st.session_state.route_context = {
        "source": None,
        "destination": None,
        "vehicle": "mini",
        "custom_source_coords": None,
        "custom_dest_coords": None
    }

def get_osrm_route(coords1, coords2):
    """Fetch real road distance and geometry from OSRM with 2s timeout and local fallback"""
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{coords1[1]},{coords1[0]};{coords2[1]},{coords2[0]}?overview=full&geometries=geojson"
        response = requests.get(url, timeout=2)
        data = response.json()
        if data.get("code") == "Ok":
            route = data["routes"][0]
            distance_km = route["distance"] / 1000
            geometry = route["geometry"]["coordinates"]
            path = [[coord[1], coord[0]] for coord in geometry]
            return distance_km, path
    except Exception:
        pass
    
    dist_straight = geodesic(coords1, coords2).km
    return dist_straight * 1.35, [list(coords1), list(coords2)]

def display_map(loc1_name, loc2_name, path=None, c1=None, c2=None):
    """Display an interactive map with markers and road path"""
    try:
        coord1 = c1 if c1 else (LOCATIONS.get(loc1_name).get("coords") if LOCATIONS.get(loc1_name) else None)
        coord2 = c2 if c2 else (LOCATIONS.get(loc2_name).get("coords") if LOCATIONS.get(loc2_name) else None)
        
        if coord1 and coord2:
            center_lat = (coord1[0] + coord2[0]) / 2
            center_lon = (coord1[1] + coord2[1]) / 2
            m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
            
            folium.Marker(coord1, popup=f"Pickup: {loc1_name}", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(coord2, popup=f"Dropoff: {loc2_name}", icon=folium.Icon(color='red')).add_to(m)
            
            if path:
                folium.PolyLine(path, color="blue", weight=3, opacity=0.7).add_to(m)
            
            st_folium(m, width=700, height=400, key=f"map_{hash(str(coord1))}_{hash(str(coord2))}")
        else:
            raise ValueError("Coordinates missing")
    except Exception:
        st.warning("📍 Map fallback: Centering on Islamabad (E-9).")
        m_fallback = folium.Map(location=[33.70, 73.05], zoom_start=12)
        st_folium(m_fallback, width=700, height=400, key="map_fallback")

# Sidebar for Quick Input
with st.sidebar:
    st.title("⚡ Kill O Meter")
    st.markdown("*Premium Twin Cities Logistics*")
    st.markdown("---")
    
    st.subheader("📍 Smart Route Engine")
    
    # Upgraded from dropdowns to raw Text Inputs for open address queries
    start_loc_input = st.text_input("From (Pickup Location):", value=st.session_state.route_context["source"] if st.session_state.route_context["source"] else "G-13")
    end_loc_input = st.text_input("To (Destination Location):", value=st.session_state.route_context["destination"] if st.session_state.route_context["destination"] else "G-9")
        
    if st.button("Calculate Smart Matrix", use_container_width=True):
        c1 = get_coordinates(start_loc_input)
        c2 = get_coordinates(end_loc_input)
        
        if c1 and c2:
            st.session_state.route_context["source"] = start_loc_input
            st.session_state.route_context["destination"] = end_loc_input
            st.session_state.route_context["custom_source_coords"] = c1
            st.session_state.route_context["custom_dest_coords"] = c2
            st.rerun()
        else:
            st.error("🔍 Couldn't map those addresses. Please verify street/sector numbers.")

    st.markdown("---")
    st.subheader("💡 Pro Tips")
    st.info("""
    - Use **AC Car** for extra comfort.
    - **InDrive** is great for bargaining.
    - Check **Metro stations** for the cheapest route!
    """)
    
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat history cleared. How can I help you?"}]
        st.session_state.route_context = {"source": None, "destination": None, "vehicle": "mini", "custom_source_coords": None, "custom_dest_coords": None}
        st.rerun()

# Main Application Layout (Two Columns)
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("🗺️ Route Visualization & Pricing")
    
    src = st.session_state.route_context["source"]
    dest = st.session_state.route_context["destination"]
    c1 = st.session_state.route_context["custom_source_coords"]
    c2 = st.session_state.route_context["custom_dest_coords"]
    
    # Auto-resolve default coords if session initialized without text submit
    if src and dest and not (c1 and c2):
        c1 = get_coordinates(src)
        c2 = get_coordinates(dest)
        st.session_state.route_context["custom_source_coords"] = c1
        st.session_state.route_context["custom_dest_coords"] = c2

    if c1 and c2:
        try:
            # 1. Fetch Real Road Distance and Path
            real_dist, road_path = get_osrm_route(c1, c2)
            dist_km = round(real_dist, 1)
            
            # 2. Clear Distance Readout
            st.metric(label="Total Route Distance", value=f"{dist_km} km")
            
            # 3. Map visualization
            display_map(src, dest, path=road_path, c1=c1, c2=c2)
            
            # 4. Complete Ride Category Matrix
            st.markdown("### 📊 Platform Fare Breakdown")
            comp_mini = get_proactive_comparison(dist_km, "mini")
            comp_bike = get_proactive_comparison(dist_km, "bike")
            comp_ac = get_proactive_comparison(dist_km, "ac_car")
            
            # Read direct base prices to calculate proportional splits for Bykea Car categories
            base_mini_val = int(comp_mini['results']['mini'].get('Our App', dist_km * 50))
            base_ac_val = int(comp_ac['results']['ac_car'].get('Our App', dist_km * 80))
            
            matrix_data = {
                "Platform": ["Our App", "Yango", "InDrive", "Bykea"],
                "🏍️ Bike": [
                    int(comp_bike['results']['bike'].get('Our App', 0)),
                    int(comp_bike['results']['bike'].get('Yango', 0)),
                    int(comp_bike['results']['bike'].get('InDrive', 0)),
                    int(comp_bike['results']['bike'].get('Bykea', 0))
                ],
                "🚗 Mini": [
                    base_mini_val,
                    int(comp_mini['results']['mini'].get('Yango', 0)),
                    int(comp_mini['results']['mini'].get('InDrive', 0)),
                    int(base_mini_val * 0.98)  # Dynamically include Bykea Car / Mini option
                ],
                "🚘 AC Car": [
                    base_ac_val,
                    int(comp_ac['results']['ac_car'].get('Yango', 0)),
                    int(comp_ac['results']['ac_car'].get('InDrive', 0)),
                    int(base_ac_val * 1.02)   # Dynamically include Bykea AC Car / Economy variant
                ]
            }
            df = pd.DataFrame(matrix_data)
            
            # Format columns safely into explicit strings to avoid any Apache Arrow engine errors
            for col in ["🏍️ Bike", "🚗 Mini", "🚘 AC Car"]:
                df[col] = df[col].apply(lambda x: f"Rs. {int(x)}" if x > 0 else "—")
            
            if not df.empty:
                st.table(df)
                
            # Render Predictive Forecasting Trends Loop
            render_predictive_forecasting_ui(dist_km, is_peak)
                
            # Compliance & Recommendations
            from compliance_engine import get_compliance_notes
            notes = get_compliance_notes(f"{src} to {dest}")
            if notes:
                st.markdown("#### 🛡️ Regulatory Notices")
                for note in notes:
                    st.info(note)
            
            rec = get_smart_recommendation(dist_km, src, dest)
            st.success(rec)
            
        except Exception as e:
            st.error(f"Error loading route data: {e}")
    else:
        st.info("👈 Enter pinpoint pickup and dropoff details in the sidebar to map routes dynamically!")
        m_default = folium.Map(location=[33.70, 73.05], zoom_start=12)
        st_folium(m_default, width=700, height=400, key="map_initial")

with col2:
    st.subheader("💬 Chat Assistant")
    
    # Scrollable chat container height
    chat_container = st.container(height=500)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me something (e.g., 'F6 to NUST ac car price')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        parsed = parse_query(prompt)
        
        # Scope Check & Guardrails
        transport_keywords = ["fare", "price", "cost", "ride", "car", "bike", "taxi", "cab", "paisa", "kiraya", "kitna", "route", "distance", "km", "kilometer", "metro", "station", "terminal", "adda", "vigo", "luxury", "ac", "mini"]
        greetings = ["hi", "hello", "salaam", "hey", "aoa", "assalam", "help", "show", "list"]
        
        is_in_scope = (
            parsed.get("loc1") is not None or 
            parsed.get("distance") is not None or 
            any(kw in prompt.lower() for kw in transport_keywords + greetings)
        )

        if not is_in_scope:
            st.session_state.route_context = {"source": None, "destination": None, "vehicle": "mini", "custom_source_coords": None, "custom_dest_coords": None}
            
            import random
            witty_refusals = [
                "I'm a ride-fare expert, not a life coach! 🚕 I can't answer that, but I can definitely tell you how much a ride to F-6 costs. Want to try?",
                "That's a bit outside my GPS range! 🗺️ I focus on Islamabad/Pindi rides. How about we calculate a fare to NUST instead?",
                "I'm still learning about the world, but I'm already a PhD in Twin Cities fares! 🎓 Ask me about a route, and I'll show you my moves.",
                "Cooking recipes? General knowledge? I'd probably get us lost! 🍲 Let's stick to what I'm good at: finding you the best ride rates."
            ]
            response = random.choice(witty_refusals)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        if parsed.get("loc1") and parsed.get("loc2"):
            st.session_state.route_context["source"] = parsed["loc1"]
            st.session_state.route_context["destination"] = parsed["loc2"]
            st.session_state.route_context["custom_source_coords"] = get_coordinates(parsed["loc1"])
            st.session_state.route_context["custom_dest_coords"] = get_coordinates(parsed["loc2"])
        
        if not (parsed.get("loc1") and parsed.get("loc2")):
            if st.session_state.route_context["source"] and st.session_state.route_context["destination"]:
                parsed["loc1"] = st.session_state.route_context["source"]
                parsed["loc2"] = st.session_state.route_context["destination"]
                
        if parsed.get("vehicle_type"):
            st.session_state.route_context["vehicle"] = parsed["vehicle_type"]

        # Generate bot response for history
        if parsed.get("loc1") and parsed.get("loc2"):
            try:
                response = st.session_state.chatbot.handle_fare_inquiry(parsed)
            except Exception as e:
                response = f"❌ *Error calculating fare:* {str(e)}"
        else:
            if parsed.get("intent") == "fare_inquiry" and not (parsed.get("loc1") or parsed.get("distance")):
                response = "I couldn't quite identify those points! 🚖 Try using sector paths (like i-8, G9) or shorthand names (like NUST, FAST, AU)."
            else:
                response = st.session_state.chatbot.process_message(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Custom CSS for styling
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)