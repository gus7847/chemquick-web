# backend/app/routers/convection.py

from fastapi import APIRouter, HTTPException
from ..models.convection_models import ConvectionInput
from ..models.response_models import ApiResponse
from ..services.convection_service import perform_convection_calculation

router = APIRouter(
    prefix="/convection",
    tags=["Convection"]
)

@router.post("/calculate", response_model=ApiResponse)
async def calculate_convection(input_data: ConvectionInput):
    try:
        # Llamar a la función de servicio para realizar los cálculos
        data = perform_convection_calculation(input_data)
        # Devolver una respuesta exitosa con los datos calculados
        return ApiResponse(message="Success", data=data)
    except ValueError as e:
        # Manejar errores de validación o cálculos específicos
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Manejar errores inesperados
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
