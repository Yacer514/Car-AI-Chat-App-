import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import datetime

# 1. SETUP: Configure page and state (MUST be the absolute first command)
st.set_page_config(
    page_title="Kill O Meter - Smart Fare Matrix",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Late imports to ensure execution stability
from chatbot import TwinCitiesChatbot
from fare_database import LOCATIONS, get_location_info, get_fare_estimate, get_proactive_comparison
from validators import parse_query

# Initialize persistent memory state across application reruns
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "route_info" not in st.session_state:
    st.session_state.route_info = {"src": None, "dst": None, "vehicle": "mini"}
if "chatbot" not in st.session_state:
    st.session_state.chatbot = TwinCitiesChatbot()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "🇵🇰 **Salaam!** Enter a route or ask me about fares, food points, or areas!"}
    ]

# 2. THEME & STYLING: Premium High-Contrast Solid Dark Theme
st.markdown("""
<style>
    /* Clean Solid Deep Slate Background for entire App layout */
    .stApp { background-color: #0F172A !important; }
    
    /* Text elements styling */
    .stApp, .stMarkdown, .stMetric, h1, h2, h3, h4, h5, h6, p, span, label { 
        color: #F8FAFC !important; 
    }
    
    /* Dark Solid Slate Cards for Main Content Components */
    .glass-card { 
        background-color: #1E293B !important; 
        border: 2px solid #334155 !important; 
        padding: 22px; 
        border-radius: 12px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    /* Light UI Styling override for Sidebar accessibility compatibility */
    [data-testid="stSidebar"] { background-color: #F1F5F9 !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p { 
        color: #0F172A !important; 
        font-weight: bold !important; 
    }
    
    /* Chat message bubble text normalization override */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span {
        color: #0F172A !important;
    }
</style>
""", unsafe_allow_html=True)


# 3. SIDEBAR CONTROLS: Intuitive route setup selectors
with st.sidebar:
    st.header("🚕 Logistics Controls")
    
    # Get alphabetical list of known points for selection comfort
    known_locations = sorted(list(LOCATIONS.keys()))
    
    src_select = st.selectbox("Select Pickup Point:", known_locations, index=known_locations.index("G-13") if "G-13" in known_locations else 0)
    dst_select = st.selectbox("Select Destination Point:", known_locations, index=known_locations.index("Saddar") if "Saddar" in known_locations else 0)
    
    vehicle_select = st.selectbox(
        "Preferred Transport Type:", 
        ["bike", "mini", "ac_car", "luxury"], 
        format_func=lambda x: "🏍️ Bike" if x == "bike" else ("🚗 Mini Car" if x == "mini" else ("❄️ AC Car" if x == "ac_car" else "✨ Luxury Car"))
    )
    
    st.markdown("---")
    if st.button("Calculate Smart Matrix", use_container_width=True):
        st.session_state.show_results = True
        st.session_state.route_info = {
            "src": src_select,
            "dst": dst_select,
            "vehicle": vehicle_select
        }
        
        # Proactively push an analytical entry into chat to complement workspace changes
        contextual_query = f"{src_select} to {dst_select} by {vehicle_select}"
        bot_response = st.session_state.chatbot.process_message(contextual_query)
        st.session_state.chat_history.append({"role": "user", "content": f"Calculate route: {src_select} to {dst_select}."})
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})


# 4. MAIN USER INTERFACE WORKSPACE (Split columns 60/40)
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.markdown('<div class="glass-card"><h3>🗺️ Route Engine Dashboard</h3>', unsafe_allow_html=True)
    
    if st.session_state.show_results:
        s_name, s_info = get_location_info(st.session_state.route_info["src"])
        d_name, d_info = get_location_info(st.session_state.route_info["dst"])
        v_type = st.session_state.route_info["vehicle"]
        
        if s_info and d_info:
            # Generate accurate matrix calculations from your core database architecture
            estimate = get_fare_estimate(v_type, s_name, d_name)
            
            # Metric Rows
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric("Estimated Distance", f"{estimate['distance_km']} KM")
            with m_col2:
                st.metric("Base Fare Pricing", f"Rs. {estimate['estimated_fare']}")
            with m_col3:
                st.metric("Surge Factor", f"{estimate['surge_multiplier']}x")
                
            st.markdown(f"**Selected Path:** `{s_name}` ➡️ `{d_name}` using **{v_type.upper()}** profile mode.")
            
            # --- GEO-MAPPING INTERACTIVE SEGMENT ---
            try:
                # Calculate geographical bounding midpoint
                mid_lat = (s_info["coords"][0] + d_info["coords"][0]) / 2
                mid_lon = (s_info["coords"][1] + d_info["coords"][1]) / 2
                
                # Render interactive Folium Map
                m = folium.Map(location=[mid_lat, mid_lon], zoom_start=12, tiles="OpenStreetMap")
                
                # Markers placement with custom design indicators
                folium.Marker(
                    location=s_info["coords"], 
                    popup=f"Origin: {s_name}", 
                    icon=folium.Icon(color="green", icon="play")
                ).add_to(m)
                
                folium.Marker(
                    location=d_info["coords"], 
                    popup=f"Destination: {d_name}", 
                    icon=folium.Icon(color="red", icon="stop")
                ).add_to(m)
                
                # Draw linear route visual connection vector
                folium.PolyLine(
                    locations=[s_info["coords"], d_info["coords"]], 
                    color="#38BDF8", 
                    weight=5, 
                    opacity=0.85
                ).add_to(m)
                
                # Display output layer securely
                st_folium(m, width="100%", height=400, key="routing_map")
                
            except Exception as geo_err:
                st.warning(f"Map plotting limitation encountered: {geo_err}")
        else:
            st.error("Error matching spatial coordinates inside application records configuration context.")
    else:
        # Prompt state display window placeholder text
        st.info("💡 Select your route parameters via the sidebar controls and hit **'Calculate Smart Matrix'** to display geospatial paths and pricing comparisons!")
        
    st.markdown('</div>', unsafe_allow_html=True)


with col2:
    st.markdown('<div class="glass-card"><h3>💬 AI Fare Companion</h3>', unsafe_allow_html=True)
    
    # Establish a clean layout scrollable containment box for the history logs
    chat_box = st.container(height=420)
    
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # Direct input text box handling layer for conversational requests
    if chat_prompt := st.chat_input("Ask: 'G-13 to Saddar bike fare' or 'Show pindi areas'"):
        if chat_prompt.strip():
            # Commit user request entry
            st.session_state.chat_history.append({"role": "user", "content": chat_prompt})
            
            # Request backend intelligence engine review
            parsed_query_object = parse_query(chat_prompt)
            
            # Check if text input contains alternative complete location routing details
            if parsed_query_object.get("loc1") and parsed_query_object.get("loc2"):
                loc1_verified, _ = get_location_info(parsed_query_object["loc1"])
                loc2_verified, _ = get_location_info(parsed_query_object["loc2"])
                
                if loc1_verified and loc2_verified:
                    # Update Map parameters dynamically based on conversational entries!
                    st.session_state.show_results = True
                    st.session_state.route_info = {
                        "src": loc1_verified,
                        "dst": loc2_verified,
                        "vehicle": parsed_query_object.get("vehicle_type") or "mini"
                    }
            
            # Generate response narrative
            answer = st.session_state.chatbot.process_message(chat_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)