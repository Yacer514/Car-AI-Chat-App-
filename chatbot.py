"""
Islamabad & Rawalpindi Ride Fare Chatbot Brain
Handles logic, intent, and proactive data delivery.
"""

from fare_database import (
    get_all_locations, get_locations_by_category, get_locations_by_city,
    get_fare_estimate, get_proactive_comparison, calculate_fare
)
from validators import parse_query
from compliance_engine import get_compliance_notes

class TwinCitiesChatbot:
    def __init__(self):
        self.locations = get_all_locations()

    def process_message(self, user_input):
        """Main entry point for processing messages"""
        if not user_input.strip():
            return "Bhai, kuch to likho! (Type something! 😊)"
            
        parsed = parse_query(user_input)
        intent = parsed.get("intent")
        
        if intent == "help":
            return self.handle_help()
        elif intent == "list_places":
            return self.handle_list_places(user_input)
        else:
            return self.handle_fare_inquiry(parsed)

    def handle_help(self):
        return """
🚕 *Twin Cities Ride Guide - Help* 🚕
━━━━━━━━━━━━━━━━━━━━━━━━━━
I can help you find fares for Cars, AC Cars, Luxury rides, and Bikes!

📍 *Try asking like this:*
• "Savour Saddar se Centaurus kitna hoga?"
• "F-6 to Saddar AC car price"
• "Pindi to Isloo bike fare"
• "Show me food points in Pindi"
• "List metro stations"

🚗 *Vehicles:* Bike, Car, AC Car, Luxury
🏙️ *Cities:* Islamabad & Rawalpindi (Pindi)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Just type your route and I'll give you all prices!
        """

    def handle_list_places(self, query):
        query = query.lower()
        
        # Check for categories
        categories = ["food", "metro", "park", "sector", "area", "landmark"]
        for cat in categories:
            if cat in query:
                locs = get_locations_by_category(cat)
                names = ", ".join(locs.keys())
                return f"📍 *{cat.capitalize()} Points:*\n\n{names}\n\nAsk me for the fare to any of these! 😊"
        
        # Check for cities
        if "pindi" in query or "rawalpindi" in query:
            locs = get_locations_by_city("Rawalpindi")
            return f"🏙️ *Rawalpindi Areas:*\n\n{', '.join(locs.keys())}"
        
        if "islamabad" in query or "isloo" in query:
            locs = get_locations_by_city("Islamabad")
            return f"🏙️ *Islamabad Areas:*\n\n{', '.join(locs.keys())}"
            
        return "Which places should I show? (e.g., 'list food points' or 'show pindi areas')"

    def handle_fare_inquiry(self, parsed):
        loc1 = parsed.get("loc1")
        loc2 = parsed.get("loc2")
        vehicle = parsed.get("vehicle_type") or "mini"
        distance = parsed.get("distance")
        
        # If we have both locations
        if loc1 and loc2:
            estimate = get_fare_estimate(vehicle, loc1, loc2)
            if estimate:
                # Add compliance check
                compliance_query = f"Ride from {loc1} to {loc2} by {vehicle}"
                estimate["compliance_notes"] = get_compliance_notes(compliance_query)
                return self._format_comprehensive_response(estimate)
        
        # If we only have distance
        if distance:
            comparison = get_proactive_comparison(distance, vehicle)
            return self._format_distance_response(comparison)
            
        # If we have one location but not two
        if loc1:
            return f"I found *{loc1}*, but where are you going? (e.g., '{loc1} to Saddar')"

        return "I didn't quite catch the locations. Try: 'F-6 to Saddar' or '10km bike fare'."

    def _format_comprehensive_response(self, estimate):
        dist = estimate['distance_km']
        vehicle = estimate['vehicle_type']
        
        # Get comparison for this distance
        comp = get_proactive_comparison(dist, vehicle)
        res = comp['results'][vehicle]
        
        surge_notes = []
        if estimate.get('is_monsoon'):
            surge_notes.append("⚠️ *Monsoon Surge (+40%) Included*")
        if estimate.get('is_peak'):
            surge_notes.append("🚦 *Peak Hour Surge (+30%) Included*")
            
        surge_text = "\n".join(surge_notes)
        
        v_label = vehicle.upper().replace('_', ' ')
        if vehicle == "mini": v_label = "Mini Car"
        elif vehicle == "ac_car": v_label = "AC Car"
        
        response = f"""
💰 *Fare Breakdown* ({dist} km)
━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 *From:* {estimate['from']}
📍 *To:* {estimate['to']}
🚗 *Type:* {v_label}

💵 *Platform Estimates:*
"""
        for platform, price in res.items():
            cheapest = "✨" if platform == "InDrive" or (platform == "Bykea" and vehicle == "bike") else ""
            response += f"• {platform:.<15} Rs. {price} {cheapest}\n"
            
        compliance_text = ""
        if estimate.get("compliance_notes"):
            compliance_text = "\n🛡️ *Security & Compliance:* \n"
            for note in estimate["compliance_notes"]:
                compliance_text += f"• {note}\n"
            
        response += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━
{surge_text}{compliance_text}
*Pro Tip:* InDrive is usually cheaper for bargaining! 😉
"""
        return response

    def _format_distance_response(self, comparison):
        dist = comparison['distance']
        response = f"💰 *Estimates for {dist} km:*\n\n"
        
        for v_type, rates in comparison['results'].items():
            response += f"*{v_type.upper()}:*\n"
            for platform, price in rates.items():
                response += f"• {platform}: Rs. {price}\n"
            response += "\n"
            
        return response + "━━━━━━━━━━━━━━━━━━━━━━━━━━\nPrices may vary based on traffic! 🚦"
