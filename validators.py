"""
Input validation and parsing utilities with informal language support
"""

import re
import difflib
from fare_database import get_all_locations, FARE_CONFIG

def validate_vehicle_type(vehicle_input):
    """Normalize vehicle type including Mini, AC and Luxury options"""
    v_lower = vehicle_input.strip().lower()
    
    # AC Car
    if any(kw in v_lower for kw in ['ac', 'air condition', 'premium']):
        return 'ac_car'
    
    # Luxury
    if any(kw in v_lower for kw in ['luxury', 'vigo', 'civic', 'fortuner', 'prado', 'audi']):
        return 'luxury'
    
    # Bike
    if any(kw in v_lower for kw in ['bike', 'motorcycle', 'bykea', '2-wheeler', 'moto']):
        return 'bike'
    
    # Mini Car / Standard
    if any(kw in v_lower for kw in ['mini', 'small', 'standard', 'car', 'taxi', 'cab', 'sedan', 'auto', 'ride']):
        return 'mini'
    
    return None

def get_closest_location(query):
    """Find the closest matching location from the database using fuzzy matching"""
    locations = get_all_locations()
    query_upper = query.upper()
    
    # Try exact or partial matches first
    for loc in locations:
        if query_upper == loc.upper() or query_upper in loc.upper():
            return loc
            
    # Fuzzy matching
    matches = difflib.get_close_matches(query, locations, n=1, cutoff=0.6)
    return matches[0] if matches else None

def normalize_sector(text):
    """Normalize variations like i8, I8, i 8 to I-8"""
    # Pattern to match sector letter and number (e.g., F6, G-11, i 8)
    match = re.search(r'([a-jA-J])\s*-?\s*(\d{1,2})', text)
    if match:
        letter = match.group(1).upper()
        number = match.group(2)
        return f"{letter}-{number}"
    return text

def map_shorthand(text):
    """Map local shorthand to descriptive location names"""
    shorthand_map = {
        "AU": "Air University",
        "BU": "Bahria University",
        "NUST": "NUST H-12 Campus",
        "FAST": "FAST-NU H-11",
        "ARID": "Arid Agriculture University",
        "FM": "Faisal Movers Terminal",
        "DAEWOO": "Daewoo Express Terminal",
        "KORANG": "Korang Transport Hub",
        "FAIZABAD": "Faizabad Interchange Terminal",
        "ISB AIRPORT": "Islamabad International Airport",
        "AIRPORT": "Islamabad International Airport"
    }
    
    result = text.upper()
    # Sort keys by length descending to match 'ISB AIRPORT' before 'AIRPORT'
    for short, long in sorted(shorthand_map.items(), key=lambda x: len(x[0]), reverse=True):
        # Use word boundaries to avoid partial matches (like 'FA' in 'FAST')
        result = re.sub(rf'\b{re.escape(short)}\b', long, result)
            
    return result

def clean_address(text):
    """Clean punctuation and normalize address for geocoding"""
    # Strip excessive punctuation but keep forward slashes for sub-sectors (e.g., G13/4)
    cleaned = re.sub(r'[^\w\s/]', '', text)
    # Append Islamabad if not present for better geocoding resolution
    if "islamabad" not in cleaned.lower() and "rawalpindi" not in cleaned.lower():
        cleaned += ", Islamabad"
    return cleaned.strip()

def parse_query(user_input):
    """
    Parse user query with robust address handling and normalization.
    """
    # Basic cleaning
    query_raw = user_input.strip()
    # Sector Normalization (e.g., i8 -> I-8, g13/4 -> G-13/4)
    query_normalized = re.sub(r'([a-jA-J])\s*-?\s*(\d{1,2}(?:/\d)?)', 
                             lambda m: f"{m.group(1).upper()}-{m.group(2)}", 
                             query_raw)
    
    query_mapped = map_shorthand(query_normalized)
    query_lower = query_mapped.lower()
    
    result = {
        "vehicle_type": validate_vehicle_type(query_lower),
        "loc1": None,
        "loc2": None,
        "distance": None,
        "intent": "fare_inquiry",
        "raw_query": query_mapped
    }
    
    # Intent detection
    if any(kw in query_lower for kw in ["list", "show", "tell", "available", "categories", "where"]):
        result["intent"] = "list_places"
    elif any(kw in query_lower for kw in ["help", "guide", "how to"]):
        result["intent"] = "help"
    
    # Extract locations from system database first
    locations = get_all_locations()
    found_locs = []
    sorted_locs = sorted(locations, key=len, reverse=True)
    
    temp_query = query_lower
    for loc in sorted_locs:
        loc_l = loc.lower()
        if loc_l in temp_query:
            found_locs.append(loc)
            temp_query = temp_query.replace(loc_l, " [LOC] ")
            
    # Advanced Address Extraction: 
    # If we don't have 2 system locations, look for "from X to Y" pattern
    if len(found_locs) < 2:
        route_match = re.search(r'(?:from|pickup|at)\s+(.+?)\s+(?:to|dropoff|for)\s+(.+)', query_mapped, re.IGNORECASE)
        if route_match:
            # Only use these if they aren't already matched as system locs
            addr1 = route_match.group(1).strip()
            addr2 = route_match.group(2).strip()
            # Clean them
            result["loc1"] = clean_address(addr1)
            result["loc2"] = clean_address(addr2)
            return result

    if len(found_locs) >= 1:
        result["loc1"] = found_locs[0]
    if len(found_locs) >= 2:
        result["loc2"] = found_locs[1]
        
    # Extract distance
    dist_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|k\.m|kilometers?|kms?)', query_lower)
    if dist_match:
        result["distance"] = float(dist_match.group(1))
        
    return result
