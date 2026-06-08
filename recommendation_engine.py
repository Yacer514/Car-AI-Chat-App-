import google.generativeai as genai
import os

# To use Gemini, the user needs to set the GEMINI_API_KEY environment variable
# For now, I'll provide a fallback/heuristic recommendation if the key is missing.

def get_smart_recommendation(distance, loc1, loc2, vehicle_type=None):
    """
    Generate a smart contextual recommendation using Gemini (or fallback)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    prompt = f"""
    As a local transport expert for Islamabad and Rawalpindi, advise a user on their ride.
    Route: From {loc1} to {loc2}
    Distance: {distance} km
    Transport modes: Car and Bike
    
    Current conditions: Consider typical congestion, sector types (residential vs commercial), and distance.
    Provide a concise (2-3 sentences) recommendation on whether they should take a car or bike.
    If the distance is > 10km, mention comfort. If it's < 5km, mention cost-effectiveness of bikes.
    Mention specific landmarks or sectors if relevant.
    """

    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Heuristic Advice: For a {distance}km trip from {loc1} to {loc2}, a {'bike is faster in traffic' if distance < 8 else 'car is better for comfort'}. Stay safe!"
    else:
        # Heuristic fallback
        if distance < 5:
            return f"💡 *Recommendation:* For this short {distance}km trip, a **Bike** is your best bet! It's cheaper and will zip through any narrow streets or signals between {loc1} and {loc2}."
        elif distance > 15:
            return f"💡 *Recommendation:* Since you're traveling {distance}km across the Twin Cities, we recommend an **AC Car**. It will be much more comfortable for this long distance, especially if you're heading towards {loc2}."
        else:
            return f"💡 *Recommendation:* At {distance}km, both modes are fine. Take a **Bike** if you're in a hurry to beat traffic, or a **Car** if you want to avoid the sun and dust."

if __name__ == "__main__":
    print(get_smart_recommendation(12, "F-6", "Saddar"))
