import json
import os
from models import Patient
import google.generativeai as genai

def get_api_key():
    # Look for config.json in the project root
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            if config.get("GEMINI_API_KEY"):
                return config.get("GEMINI_API_KEY")
    return os.environ.get("GEMINI_API_KEY")

class IntakeExtractorAgent:
    def __init__(self, model_name="models/gemini-3.5-flash"):
        api_key = get_api_key()
        if not api_key:
            print("Warning: Could not initialize Gemini API Key. Make sure GEMINI_API_KEY is set in config.json.")
        else:
            genai.configure(api_key=api_key)
        self.model_name = model_name

    def extract(self, clinical_note: str) -> Patient:
        """Uses Gemini to extract structured patient data from a clinical note."""
        print(f"Extracting patient details using {self.model_name}...")
        
        # Initialize the model
        model = genai.GenerativeModel(self.model_name)
        
        prompt = f"""
You are a medical intake extractor agent. Read the provided clinical note and extract the patient's ABCDE status (Airway, Breathing, Circulation, Disability, Exposure), expected resources needed (0, 1, 2, or 3+), and a summary of vitals. Infer status based on the notes if not explicitly stated. If a name is not present in the text, use 'Unknown Patient'.

Clinical Note:
{clinical_note}
"""
        # We can pass the Pydantic model directly to Gemini's generation_config
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=Patient
            )
        )
        
        # The response text will be a JSON string matching the Patient schema
        return Patient.model_validate_json(response.text)
