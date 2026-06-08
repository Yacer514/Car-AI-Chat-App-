"""
Twin Cities Ride Fare Database (Islamabad & Rawalpindi)
Contains fare rates and locations for the Twin Cities.
Pricing based on Indrive, Yango, and Bykea.
Uses Faizabad as the central 0-point for distance estimation.
"""

from datetime import datetime

# FARE_CONFIG: Base fares and per-km rates for different vehicle types
# Multipliers: mini (Standard), ac_car (Premium), bike (Economical)
FARE_CONFIG = {
    "mini": {
        "base_fare": 180,
        "per_km_rate": 35,
        "minimum_fare": 350
    },
    "ac_car": {
        "base_fare": 300,
        "per_km_rate": 50,
        "minimum_fare": 500
    },
    "bike": {
        "base_fare": 80,
        "per_km_rate": 10,
        "minimum_fare": 120
    },
    "luxury": {
        "base_fare": 500,
        "per_km_rate": 80,
        "minimum_fare": 1000
    }
}

# Monsoon season surge (July-September)
MONSOON_MONTHS = [7, 8, 9]
MONSOON_SURGE_MULTIPLIER = 1.40

# Peak hours: 8-10 AM and 5-7 PM
PEAK_HOURS = [(8, 10), (17, 19)]
PEAK_SURGE_MULTIPLIER = 1.30

def is_peak_hour():
    """Check if the current time is within peak hours"""
    current_hour = datetime.now().hour
    for start, end in PEAK_HOURS:
        if start <= current_hour < end:
            return True
    return False

# LOCATIONS: Signed distance from Faizabad (0 point)
# Islamabad: Positive values | Rawalpindi: Negative values
LOCATIONS = {
    # --- Metro Stations (Red Line) ---
    "Saddar Metro": {"city": "Rawalpindi", "category": "metro", "dist": -13.5, "coords": (33.5973, 73.0487)},
    "Pindi Station": {"city": "Rawalpindi", "category": "landmark", "dist": -14.0, "coords": (33.5912, 73.0538)},
    "Islamabad Station": {"city": "Islamabad", "category": "landmark", "dist": 5.0, "coords": (33.6593, 73.0125)},
    "Marrir Chowk Metro": {"city": "Rawalpindi", "category": "metro", "dist": -12.0, "coords": (33.6062, 73.0583)},
    "Liaquat Bagh Metro": {"city": "Rawalpindi", "category": "metro", "dist": -10.5, "coords": (33.6144, 73.0655)},
    "Committee Chowk Metro": {"city": "Rawalpindi", "category": "metro", "dist": -9.0, "coords": (33.6214, 73.0715)},
    "Waris Khan Metro": {"city": "Rawalpindi", "category": "metro", "dist": -7.5, "coords": (33.6284, 73.0775)},
    "Chandni Chowk Metro": {"city": "Rawalpindi", "category": "metro", "dist": -6.0, "coords": (33.6354, 73.0835)},
    "Rehmanabad Metro": {"city": "Rawalpindi", "category": "metro", "dist": -4.5, "coords": (33.6424, 73.0895)},
    "6th Road Metro": {"city": "Rawalpindi", "category": "metro", "dist": -3.0, "coords": (33.6494, 73.0955)},
    "Shamsabad Metro": {"city": "Rawalpindi", "category": "metro", "dist": -1.5, "coords": (33.6564, 73.1015)},
    "Faizabad Interchange Terminal": {"city": "Both", "category": "transit", "dist": 0.0, "coords": (33.6634, 73.0831)},
    "IJP Metro": {"city": "Islamabad", "category": "metro", "dist": 1.5, "coords": (33.6704, 73.0771)},
    "Potohar Metro": {"city": "Islamabad", "category": "metro", "dist": 3.0, "coords": (33.6774, 73.0711)},
    "Khayaban-e-Johar Metro": {"city": "Islamabad", "category": "metro", "dist": 4.5, "coords": (33.6844, 73.0651)},
    "Faiz Ahmed Faiz Metro": {"city": "Islamabad", "category": "metro", "dist": 6.0, "coords": (33.6914, 73.0591)},
    "Kashmir Highway Metro": {"city": "Islamabad", "category": "metro", "dist": 7.5, "coords": (33.6984, 73.0531)},
    "Chaman Metro": {"city": "Islamabad", "category": "metro", "dist": 9.0, "coords": (33.7054, 73.0471)},
    "Ibn-e-Sina Metro": {"city": "Islamabad", "category": "metro", "dist": 10.5, "coords": (33.7124, 73.0411)},
    "Katchehry Metro": {"city": "Islamabad", "category": "metro", "dist": 12.0, "coords": (33.7194, 73.0351)},
    "PIMS Metro": {"city": "Islamabad", "category": "metro", "dist": 13.5, "coords": (33.7264, 73.0291)},
    "Stock Exchange Metro": {"city": "Islamabad", "category": "metro", "dist": 15.0, "coords": (33.7334, 73.0231)},
    "7th Avenue Metro": {"city": "Islamabad", "category": "metro", "dist": 16.5, "coords": (33.7404, 73.0171)},
    "Shaheed-e-Millat Metro": {"city": "Islamabad", "category": "metro", "dist": 18.0, "coords": (33.7474, 73.0111)},
    "Parade Ground Metro": {"city": "Islamabad", "category": "metro", "dist": 19.5, "coords": (33.7544, 73.0051)},
    "Pak Secretariat": {"city": "Islamabad", "category": "metro", "dist": 21.0, "coords": (33.7614, 72.9991)},

    # --- Islamabad Sectors ---
    "F-6": {"city": "Islamabad", "category": "sector", "dist": 18.0, "coords": (33.7319, 73.0673)},
    "F-7": {"city": "Islamabad", "category": "sector", "dist": 17.0, "coords": (33.7214, 73.0519)},
    "F-8": {"city": "Islamabad", "category": "sector", "dist": 15.0, "coords": (33.7119, 73.0373)},
    "F-10": {"city": "Islamabad", "category": "sector", "dist": 16.0, "coords": (33.7019, 73.0073)},
    "F-11": {"city": "Islamabad", "category": "sector", "dist": 17.5, "coords": (33.6919, 72.9873)},
    "G-6": {"city": "Islamabad", "category": "sector", "dist": 15.0, "coords": (33.7119, 73.0773)},
    "G-7": {"city": "Islamabad", "category": "sector", "dist": 14.0, "coords": (33.7019, 73.0673)},
    "G-8": {"city": "Islamabad", "category": "sector", "dist": 12.0, "coords": (33.6919, 73.0573)},
    "G-9": {"city": "Islamabad", "category": "sector", "dist": 10.0, "coords": (33.6819, 73.0473)},
    "G-10": {"city": "Islamabad", "category": "sector", "dist": 11.5, "coords": (33.6719, 73.0373)},
    "G-11": {"city": "Islamabad", "category": "sector", "dist": 13.0, "coords": (33.6619, 73.0273)},
    "G-13": {"city": "Islamabad", "category": "sector", "dist": 15.0, "coords": (33.6519, 72.9973)},
    "H-8": {"city": "Islamabad", "category": "sector", "dist": 6.0, "coords": (33.6619, 73.0673)},
    "I-8": {"city": "Islamabad", "category": "sector", "dist": 3.0, "coords": (33.6419, 73.0773)},
    "I-9": {"city": "Islamabad", "category": "sector", "dist": 4.0, "coords": (33.6319, 73.0673)},
    "I-10": {"city": "Islamabad", "category": "sector", "dist": 5.0, "coords": (33.6219, 73.0573)},

    # --- Rawalpindi Areas ---
    "Saddar": {"city": "Rawalpindi", "category": "area", "dist": -13.5, "coords": (33.5973, 73.0487)},
    "Satellite Town": {"city": "Rawalpindi", "category": "area", "dist": -4.0, "coords": (33.6419, 73.0673)},
    "Commercial Market": {"city": "Rawalpindi", "category": "area", "dist": -5.0, "coords": (33.6319, 73.0773)},
    "Raja Bazar": {"city": "Rawalpindi", "category": "area", "dist": -11.0, "coords": (33.6073, 73.0587)},
    "Tench Bhata": {"city": "Rawalpindi", "category": "area", "dist": -16.0, "coords": (33.5873, 73.0387)},
    "Westridge": {"city": "Rawalpindi", "category": "area", "dist": -15.0, "coords": (33.6173, 73.0287)},
    "DHA": {"city": "Rawalpindi", "category": "area", "dist": -20.0, "coords": (33.5273, 73.1587)},
    "Bahria": {"city": "Rawalpindi", "category": "area", "dist": -25.0, "coords": (33.5073, 73.0987)},

    # --- Food Points ---
    "Centaurus": {"city": "Islamabad", "category": "landmark", "dist": 14.0, "coords": (33.7077, 73.0503)},
    "Blue Area": {"city": "Islamabad", "category": "landmark", "dist": 16.0, "coords": (33.7119, 73.0673)},
    "Savour Blue Area": {"city": "Islamabad", "category": "food", "dist": 16.0, "coords": (33.7119, 73.0673)},
    "Savour Saddar": {"city": "Rawalpindi", "category": "food", "dist": -13.5, "coords": (33.5973, 73.0487)},
    "Monal": {"city": "Islamabad", "category": "food", "dist": 25.0, "coords": (33.7573, 73.0587)},
    "Des Pardes": {"city": "Islamabad", "category": "food", "dist": 20.0, "coords": (33.7273, 73.0587)},
    "Cheezious Commercial": {"city": "Rawalpindi", "category": "food", "dist": -5.0, "coords": (33.6319, 73.0773)},
    "Cheezious F-7": {"city": "Islamabad", "category": "food", "dist": 17.0, "coords": (33.7214, 73.0519)},
    "Tehzeeb Blue Area": {"city": "Islamabad", "category": "food", "dist": 16.5, "coords": (33.7159, 73.0613)},
    "Tehzeeb 6th Road": {"city": "Rawalpindi", "category": "food", "dist": -3.5, "coords": (33.6454, 73.0915)},
    "Kartarpura": {"city": "Rawalpindi", "category": "food", "dist": -10.0, "coords": (33.6173, 73.0687)},

    # --- Parks & Landmarks ---
    "Lake View Park": {"city": "Islamabad", "category": "park", "dist": 8.0, "coords": (33.7123, 73.1234)},
    "Ayub Park": {"city": "Rawalpindi", "category": "park", "dist": -18.0, "coords": (33.5673, 73.0887)},
    "Faisal Mosque": {"city": "Islamabad", "category": "landmark", "dist": 18.0, "coords": (33.7299, 73.0373)},
    "Shakarparian": {"city": "Islamabad", "category": "park", "dist": 3.0, "coords": (33.6873, 73.0787)},
    "Pakistan Monument": {"city": "Islamabad", "category": "landmark", "dist": 4.0, "coords": (33.6933, 73.0683)},
    "Centaurus Mall": {"city": "Islamabad", "category": "landmark", "dist": 14.0, "coords": (33.7077, 73.0503)},
    "Airport": {"city": "Islamabad", "category": "airport", "dist": 35.0, "coords": (33.5593, 72.8252)},
    "Islamabad International Airport": {"city": "Islamabad", "category": "airport", "dist": 35.0, "coords": (33.5593, 72.8252)},
    "Air University": {"city": "Islamabad", "category": "university", "dist": 14.0, "coords": (33.7144, 73.0238)},
    "Bahria University": {"city": "Islamabad", "category": "university", "dist": 14.0, "coords": (33.7154, 73.0248)},
    "NUST H-12 Campus": {"city": "Islamabad", "category": "university", "dist": 10.0, "coords": (33.6425, 72.9912)},
    "FAST-NU H-11": {"city": "Islamabad", "category": "university", "dist": 9.0, "coords": (33.6454, 73.0213)},
    "Arid Agriculture University": {"city": "Rawalpindi", "category": "university", "dist": -5.0, "coords": (33.6414, 73.0813)},
    "Faisal Movers Terminal": {"city": "Rawalpindi", "category": "transit", "dist": -1.5, "coords": (33.6614, 73.0813)},
    "Daewoo Express Terminal": {"city": "Rawalpindi", "category": "transit", "dist": -8.0, "coords": (33.6214, 73.0613)},
    "Korang Transport Hub": {"city": "Rawalpindi", "category": "transit", "dist": -18.0, "coords": (33.5414, 73.1213)},
}

def get_all_locations():
    """Return list of all location names"""
    return sorted(list(LOCATIONS.keys()))

def get_locations_by_category(category):
    """Return locations filtered by category"""
    return {k: v for k, v in LOCATIONS.items() if v["category"] == category}

def get_locations_by_city(city):
    """Return locations filtered by city"""
    return {k: v for k, v in LOCATIONS.items() if v["city"] == city or v["city"] == "Both"}

def calculate_fare(vehicle_type, distance, is_monsoon=None, is_peak=None):
    """Calculate fare based on distance and vehicle type"""
    if vehicle_type not in FARE_CONFIG:
        vehicle_type = "mini"  # Default to Mini
    
    if is_monsoon is None:
        is_monsoon = datetime.now().month in MONSOON_MONTHS
        
    if is_peak is None:
        is_peak = is_peak_hour()
    
    config = FARE_CONFIG[vehicle_type]
    
    # Re-engineered pricing logic for short distances (< 1.5km)
    if distance < 1.5:
        if vehicle_type == "bike": base_fare = 100
        elif vehicle_type == "mini": base_fare = 250
        elif vehicle_type == "ac_car": base_fare = 350
        else: base_fare = config["minimum_fare"]
    else:
        raw_fare = config["base_fare"] + (distance * config["per_km_rate"])
        base_fare = max(raw_fare, config["minimum_fare"])
    
    multiplier = 1.0
    if is_monsoon:
        multiplier *= MONSOON_SURGE_MULTIPLIER
    if is_peak:
        multiplier *= PEAK_SURGE_MULTIPLIER
        
    final_fare = base_fare * multiplier
    
    return int(final_fare), is_monsoon, multiplier, is_peak

def get_location_info(name):
    """Find location info by name (case-insensitive)"""
    name_lower = name.lower()
    for loc_name, info in LOCATIONS.items():
        if loc_name.lower() == name_lower:
            return loc_name, info
    return None, None

def get_fare_estimate(vehicle_type, loc1_name, loc2_name, override_dist=None):
    """Estimate fare between two locations using signed distance or real road override"""
    name1, info1 = get_location_info(loc1_name)
    name2, info2 = get_location_info(loc2_name)
    
    if not info1 or not info2:
        return None
    
    if override_dist is not None:
        distance = override_dist
    else:
        # Calculate distance using signed points
        distance = abs(info1["dist"] - info2["dist"])
        # Add a small buffer for road curves (min 2km)
        distance = max(distance, 2.0) + 1.5
    
    fare, is_monsoon, multiplier, is_peak = calculate_fare(vehicle_type, distance)
    
    return {
        "from": name1,
        "to": name2,
        "distance_km": round(distance, 1),
        "vehicle_type": vehicle_type,
        "estimated_fare": fare,
        "is_monsoon": is_monsoon,
        "is_peak": is_peak,
        "surge_multiplier": round(multiplier, 2)
    }

def get_proactive_comparison(distance, vehicle_type=None):
    """Get comparative pricing from different platforms proactively"""
    # Categories to compare
    v_types = ["bike", "mini", "ac_car"] if not vehicle_type else [vehicle_type]
    peak_active = is_peak_hour()
    
    comparison = {
        "distance": round(distance, 1),
        "is_monsoon": datetime.now().month in MONSOON_MONTHS,
        "is_peak": peak_active,
        "results": {}
    }
    
    for v in v_types:
        if v not in FARE_CONFIG: continue
        
        base_fare, _, _, _ = calculate_fare(v, distance)
        
        # Simulated platform rates with realistic variance
        indrive = int(base_fare * 0.92)
        yango = int(base_fare * 1.08)
        
        # Expanded Bykea logic: now supports all categories
        if v == "bike":
            bykea = int(base_fare * 0.88)
        elif v == "mini":
            bykea = int(base_fare * 0.95)
        elif v == "ac_car":
            bykea = int(base_fare * 1.02)
        else:
            bykea = None
            
        platform_rates = {
            "Our App": base_fare,
            "InDrive": indrive,
            "Yango": yango
        }
        
        if bykea:
            platform_rates["Bykea"] = bykea
            
        comparison["results"][v] = platform_rates
            
    return comparison
