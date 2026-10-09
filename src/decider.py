from typing import List

class StrandsDecider:
    def __init__(self, model_name="strands-decider-2b"):
        self.model_name = model_name

    def decide(self, state: str, options: List[str]) -> str:
        """
        Strands Decider acts as a fast routing model.
        It evaluates the text-based state and picks the best option.
        """
        state_lower = state.lower()
        
        # Simulated routing logic that the 2B decision model would handle:
        if "compromised" in state_lower or "cardiac arrest" in state_lower or "unresponsive" in state_lower:
            return "Level 1: Resuscitation"
        elif "severe" in state_lower or "high risk" in state_lower or "altered" in state_lower:
            return "Level 2: Emergent"
        elif "resources: 2" in state_lower or "resources: 3" in state_lower:
            return "Level 3: Urgent"
        elif "resources: 1" in state_lower:
            return "Level 4: Less Urgent"
        else:
            return "Level 5: Non-Urgent"
