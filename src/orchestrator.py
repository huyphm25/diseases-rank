from models import Patient
from decider import StrandsDecider

class TriageOrchestrator:
    def __init__(self):
        # Strands Decider acts as the main orchestrator agent
        self.decider = StrandsDecider()
        
        # The options the decider will choose from
        self.triage_levels = [
            "Level 1: Resuscitation",
            "Level 2: Emergent",
            "Level 3: Urgent",
            "Level 4: Less Urgent",
            "Level 5: Non-Urgent"
        ]

    def format_patient_state(self, patient: Patient) -> str:
        """Formats the patient data into a clear state for the decider."""
        return (
            f"Patient: {patient.name}\n"
            f"A (Airway): {patient.airway}\n"
            f"B (Breathing): {patient.breathing}\n"
            f"C (Circulation): {patient.circulation}\n"
            f"D (Disability): {patient.disability}\n"
            f"E (Exposure): {patient.exposure}\n"
            f"Vitals: {patient.vitals}\n"
            f"Resources: {patient.resources_expected}"
        )

    def triage_patient(self, patient: Patient) -> str:
        """
        Orchestrates the triage process by passing state to the decider.
        """
        print(f"Orchestrating triage for {patient.name} using Strands Decider...")
        patient_state = self.format_patient_state(patient)
        decision = self.decider.decide(state=patient_state, options=self.triage_levels)
        return decision
