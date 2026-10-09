import json
import os
import sys
import random

# Ensure src/ is in the python path if running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extractor import IntakeExtractorAgent
from orchestrator import TriageOrchestrator
from models import Patient

def get_random_note_from_dataset(dataset_path: str) -> str:
    """Reads a random clinical note from the specified dataset."""
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}.")
        return ""

    with open(dataset_path, "r") as f:
        lines = f.readlines()
        if not lines:
            return ""
        
        # Pick a random line
        line = random.choice(lines)
        record = json.loads(line)
        note = record.get("text", "") or record.get("note", "")
        if not note:
            note = list(record.values())[0] if record else ""
        return note

def print_banner(title: str, content: str):
    """Helper to print nicely formatted banners."""
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)
    print(content)
    print("="*50 + "\n")

def run_fixed_cases(orchestrator: TriageOrchestrator):
    """Runs the triage orchestrator against 3 fixed patient scenarios."""
    print_banner("FIXED CASES", "Running 3 predefined patient cases directly through the Triage Orchestrator...")
    
    p1 = Patient(
        name="John Doe",
        airway="Compromised",
        breathing="Severe Distress",
        circulation="Shock",
        disability="Unresponsive",
        exposure="Normal",
        resources_expected=3,
        vitals="HR 140, BP 80/50, SpO2 85%"
    )
    
    p2 = Patient(
        name="Jane Smith",
        airway="Clear",
        breathing="Normal",
        circulation="Stable",
        disability="Alert",
        exposure="Normal",
        resources_expected=2,
        vitals="HR 80, BP 120/80, SpO2 98%"
    )
    
    p3 = Patient(
        name="Bob Jones",
        airway="Clear",
        breathing="Normal",
        circulation="Stable",
        disability="Alert",
        exposure="Normal",
        resources_expected=0,
        vitals="HR 70, BP 110/70, SpO2 99%"
    )
    
    for i, p in enumerate([p1, p2, p3], 1):
        print(f"--- Case {i}: {p.name} ---")
        result = orchestrator.triage_patient(p)
        print(f"Result: {result}\n")

def run_random_patient_demo(orchestrator: TriageOrchestrator):
    """Runs a random clinical note through the Extractor and then the Triage Orchestrator."""
    dataset_path = "data/dataset.jsonl"
    print_banner("RANDOM PATIENT DATASET", f"Loading a random note from {dataset_path}...")
    
    note = get_random_note_from_dataset(dataset_path)
    if not note:
        print("Failed to load clinical note.")
        return

    display_note = note[:500] + "...\n[Note truncated for display]" if len(note) > 500 else note
    print_banner("RAW CLINICAL NOTE (Snippet)", display_note)

    extractor = IntakeExtractorAgent()
    try:
        patient = extractor.extract(note)
    except Exception as e:
        print(f"Extraction failed: {e}")
        print("Please ensure your API Key is set in config.json and try again.")
        return

    print_banner("STRUCTURED PATIENT DATA (From Gemini)", patient.model_dump_json(indent=2))

    print("Passing to Strands Triage Orchestrator...\n")
    triage_result = orchestrator.triage_patient(patient)
    
    print_banner("FINAL TRIAGE DECISION", triage_result)


def run_demo():
    """Main workflow to run the triage pipeline."""
    orchestrator = TriageOrchestrator()
    
    # 1. Test 3 Fixed cases directly
    run_fixed_cases(orchestrator)
    
    # 2. Test 1 random note from the dataset
    run_random_patient_demo(orchestrator)

if __name__ == "__main__":
    run_demo()
