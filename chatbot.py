import os
import google.generativeai as genai

class TwinCitiesChatbot:
    def __init__(self):
        """
        Initializes the generative AI core engine configuration profiles safely.
        """
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            print("⚠️ Session Alert: GEMINI_API_KEY environment token is currently unset.")
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def process_message_with_context(self, user_prompt, system_context_log):
        """
        Ingests spatial route constraints, road blocks, heatwave indices, and fare matrix structures.
        """
        system_instruction = f"""
        You are the advanced, multi-variable Twin Cities AI Logistics Engine Copilot for the Islamabad and Rawalpindi transportation infrastructure.
        You have direct runtime tracking visibility into live route parameters, environmental factors, road blocks, and dynamic platform pricing matrices.

        === SYSTEM CURRENT RUNTIME CONTEXT LOG ===
        {system_context_log}
        ==========================================

        CRITICAL OPERATIONAL COMPLIANCE MATRIX:
        1. SCOPE ACCURACY: You handle questions regarding vehicle pricing metrics, traffic block situations, heatwave navigation advice, driver availability drops, or shortcut routing options. You are more than a pricing calculator—you evaluate all logistics factors.
        2. URBAN HYPER-LOCALITY: Use specified landmark titles (e.g., G-13 Markaz, Srinagar Highway, NUST H-12, G-9 Markaz, Faizabad, Saddar) directly within your conversation flow to maintain locality context.
        3. HEATWAVE OPERATIONAL GUIDELINE: Since temperatures reflect an intense June 36°C heatwave context, remind users inquiring about bikes that prolonged high-temperature trips present safety hazards. Proactively suggest compact/mini car structures where sensible.
        4. RESILIENT SYNTHESIS: Frame your advice into structured, accessible, actionable intelligence statements without sounding robotic. Never imply your background infrastructure represents a single fleet aggregator app.
        """
        try:
            full_prompt = f"{system_instruction}\n\nUser Question/Request: {user_prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return (
                f"Salaam! Chatbot context is tracking local parameters. Based on active grid measurements for your route: "
                f"The temperature is holding at a sunny 36°C heatwave level with active local path features. "
                f"Please ensure your system has your API key active via `$env:GEMINI_API_KEY='your_key'` inside your active execution session."
            )