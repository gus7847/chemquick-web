from pydantic import BaseModel
from typing import Optional

class ConvectionInput(BaseModel):
    thickness: float
    thermal_diffusivity: Optional[float] = None # Puede ser opcional si se calcula internamente
    conductivity_coefficient: float
    convection_coefficient: float
    initial_temperature: float
    ambient_temperature: float
    density: float
    specific_heat: float
    distance: float
    time: float
    iterations: int
    biot: Optional[float] = None  # Puede ser opcional si se calcula internamente
    geometry: str  # Puede ser 'plate', 'cylinder' o 'sphere'