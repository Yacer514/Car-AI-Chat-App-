import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from chatbot import TwinCitiesChatbot
from fare_database import LOCATIONS, get_proactive_comparison
from validators import parse_query

# 1. Page Configuration - MUST be first
st.set_page_config(
    page_title="Kill O Meter - Smart Fare Matrix",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Premium High-Contrast Solid Theme
st.markdown("""
<style>
    .stApp { background-color: #0F172A !important; }
    .glass-card {
        background-color: #1E293B !important;
        border: 2px solid #334155 !important;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .glass-card h1, .glass-card h2, .glass-card h3, .glass-card p, .glass-card span {
        color: #F8FAFC !important;
    }
    .traffic-card {
        background: #2D3748; 
        border-left: 5px solid #F97316; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 15px;
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] h2 { color: #0F172A !important; }
</style>
""", unsafe_allow_html=True)

# 3. Persistent State Management
if "learned_locations" not in st.session_state:
    st.session_state.learned_locations = {
        "NUST, H-12, Islamabad": (33.6428, 72.9904),
        "Saddar Commercial Center, Rawalpindi": (33.5960, 73.0531),
    }
if "chatbot" not in st.session_state:
    st.session_state.chatbot = TwinCitiesChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salaam! Ask me any fare or routing questions."}]
if "route_context" not in st.session_state:
    st.session_state.route_context = {"source": "", "destination": "", "custom_source_coords": None, "custom_dest_coords": None}

# 4. Logic Functions
def get_coordinates(address_text):
    geolocator = Nominatim(user_agent="kill_o_meter")
    try:
        location = geolocator.geocode(address_text + ", Islamabad")
        return (location.latitude, location.longitude) if location else None
    except:
        return None

def get_osrm_route(c1, c2):
    # Fallback to geodesic if OSRM is unreachable
    return geodesic(c1, c2).km * 1.35, [list(c1), list(c2)]

# 5. UI Layout
st.title("⚡ Kill O Meter")

with st.sidebar:
    st.header("Logistics Controls")
    final_src = st.text_input("Pickup Location", "NUST, Islamabad")
    final_dst = st.text_input("Destination Location", "Saddar, Rawalpindi")
    if st.button("Calculate Smart Matrix"):
        st.session_state.route_context.update({
            "source": final_src, "destination": final_dst,
            "custom_source_coords": get_coordinates(final_src),
            "custom_dest_coords": get_coordinates(final_dst)
        })
        st.rerun()

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.markdown('<div class="glass-card"><h3>🗺️ Route Dashboard</h3>', unsafe_allow_html=True)
    c1, c2 = st.session_state.route_context["custom_source_coords"], st.session_state.route_context["custom_dest_coords"]
    if c1 and c2:
        dist, _ = get_osrm_route(c1, c2)
        st.metric("Distance", f"{round(dist, 1)} km")
        # Add map here
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card"><h3>💬 AI Companion</h3>', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("Ask about fares..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = st.session_state.chatbot.process_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()