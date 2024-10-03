# backend/app/models/result_models.py

from pydantic import BaseModel
from .calculation_models import CalculationResult
from .lambda_model import LambdaValues

class DataResult(BaseModel):
    thickness: float
    thermal_diffusivity: float
    conductivity_coefficient: float
    convection_coefficient: float
    initial_temperature: float
    ambient_temperature: float
    density: float
    specific_heat: float
    distance: float
    time: float
    iterations: int
    biot: float
    geometry: str
    q_max: float
    calc1: CalculationResult
    calc2: CalculationResult
    calc3: CalculationResult
    lamb: LambdaValues
    value_a: float
    value_theta_o: float
    value_theta: float
    value_q: float
    tem: float
    q: float
