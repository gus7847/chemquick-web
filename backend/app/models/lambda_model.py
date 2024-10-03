# backend/app/models/lambda_model.py

from pydantic import BaseModel

class LambdaValues(BaseModel):
    lambda1: float
    lambda2: float
    lambda3: float
