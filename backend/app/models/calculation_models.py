# backend/app/models/calculation_models.py

from pydantic import BaseModel

class CalculationResult(BaseModel):
    value_a: float
    value_theta_o: float
    value_theta: float
    value_q: float
