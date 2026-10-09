from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str
    airway: str = Field(description="Airway status (e.g., Clear, Compromised)")
    breathing: str = Field(description="Breathing status (e.g., Normal, Severe Distress)")
    circulation: str = Field(description="Circulation status (e.g., Stable, Shock)")
    disability: str = Field(description="Disability/Neurological status (e.g., Alert, Unresponsive)")
    exposure: str = Field(description="Exposure/Environment (e.g., Normal, Hypothermia)")
    resources_expected: int = Field(description="Number of resources expected (0, 1, 2, or more)")
    vitals: str = Field(description="Vital signs summary")
