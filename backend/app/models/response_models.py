# backend/app/models/response_models.py

from pydantic import BaseModel
from .result_models import DataResult

class ApiResponse(BaseModel):
    message: str
    data: DataResult
