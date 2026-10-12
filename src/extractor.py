import json
import os
import sys
from models import Patient
import google.generativeai as genai

def get_config_path() -> str:
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

def get_api_key():
    # Look for config.json in the project root
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                if config.get("GEMINI_API_KEY"):
                    return config.get("GEMINI_API_KEY")
        except Exception:
            pass
    return os.environ.get("GEMINI_API_KEY")

def set_api_key(api_key: str, save_to_config: bool = True) -> str:
    """Sets and configures the Gemini API key. Optionally persists it to config.json."""
    cleaned_key = api_key.strip()
    if not cleaned_key:
        raise ValueError("API key cannot be empty.")
    
    os.environ["GEMINI_API_KEY"] = cleaned_key
    genai.configure(api_key=cleaned_key)

    if save_to_config:
        config_path = get_config_path()
        config_data = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config_data = json.load(f)
            except Exception:
                config_data = {}
        config_data["GEMINI_API_KEY"] = cleaned_key
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
        print(f"Gemini API key saved to {config_path}")

    return cleaned_key

def ensure_api_key(api_key: str = None, prompt_if_interactive: bool = True):
    """Ensures a Gemini API key is configured. Prompts user or checks config if not provided."""
    if api_key:
        return set_api_key(api_key)

    current_key = get_api_key()
    if current_key:
        genai.configure(api_key=current_key)
        return current_key

    if prompt_if_interactive and hasattr(sys, "stdin") and sys.stdin.isatty():
        print("Gemini API Key was not found in config.json or environment variables.")
        try:
            entered_key = input("Please enter your Gemini API Key: ").strip()
            if entered_key:
                return set_api_key(entered_key, save_to_config=True)
        except (EOFError, KeyboardInterrupt):
            pass

    return None

class IntakeExtractorAgent:
    def __init__(self, model_name="models/gemini-3.5-flash", api_key: str = None):
        self.api_key = ensure_api_key(api_key=api_key, prompt_if_interactive=True)
        if not self.api_key:
            print("Warning: Could not initialize Gemini API Key. Use set_api_key(...) or set GEMINI_API_KEY in config.json.")
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
