# backend/app/services/convection_service.py

from ..models.result_models import DataResult
from ..models.convection_models import ConvectionInput
from ..models.calculation_models import CalculationResult
from ..models.lambda_model import LambdaValues
from ..calculations.convection_calculations import (
    InitialCalcs,
    InitialCalcsData,
    calc_qmax,
    calc_biot,
    calc_alpha,
    LambdaPlate,
    LambdaCylinder,
    LambdaSphere,
    Plate,
    Cylinder,
    Sphere,
    SumTable,
    ConvectionResults,
    FinalValues
)

def perform_convection_calculation(input_data: ConvectionInput) -> DataResult:
    # Convertir ConvectionInput a InitialCalcsData
    data = InitialCalcsData(
        thickness=input_data.thickness,
        thermal_diffusivity=input_data.thermal_diffusivity,
        conductivity_coefficient=input_data.conductivity_coefficient,
        convection_coefficient=input_data.convection_coefficient,
        initial_temperature=input_data.initial_temperature,
        ambient_temperature=input_data.ambient_temperature,
        density=input_data.density,
        specific_heat=input_data.specific_heat,
        distance=input_data.distance,
        time=input_data.time,
        iterations=input_data.iterations,
        biot=input_data.biot,
        geometry=input_data.geometry.lower()
    )

    # Crear instancia de InitialCalcs
    initial_parameters = InitialCalcs(data)

    # Calcular q_max
    if data.geometry in ["sphere", "cylinder", "plate"]:
        calcs = initial_parameters  # Ya creado
        qmax = calc_qmax(calcs, data.geometry)
    else:
        raise ValueError("Error: geometría incorrecta")
    
    # Calcular número de Biot si no se proporciona
    if calcs.biot is None or calcs.biot == 0:
        biot = calc_biot(calcs)
        calcs.biot = biot
    else:
        biot = calcs.biot

    # Calcular la difusividad térmica
    if calcs.thermal_diffusivity is None or calcs.thermal_diffusivity == 0:
        calcs.thermal_diffusivity = calc_alpha(calcs)

    # Calcular valores de lambda y realizar cálculos según la geometría
    if data.geometry == "plate":
        lamb = LambdaPlate(biot, data.iterations)
        calc1 = Plate(calcs, lamb.lambda1)
        calc2 = Plate(calcs, lamb.lambda2)
        calc3 = Plate(calcs, lamb.lambda3)
    elif data.geometry == "cylinder":
        lamb = LambdaCylinder(biot, data.iterations)
        calc1 = Cylinder(calcs, lamb.lambda1)
        calc2 = Cylinder(calcs, lamb.lambda2)
        calc3 = Cylinder(calcs, lamb.lambda3)
    elif data.geometry == "sphere":
        try:
            lamb = LambdaSphere(biot, data.iterations)
            calc1 = Sphere(calcs, lamb.lambda1)
            calc2 = Sphere(calcs, lamb.lambda2)
            calc3 = Sphere(calcs, lamb.lambda3)
        except Exception as e:
            raise ValueError(f"Error calculando lambda: {e}")
    else:
        raise ValueError("Error: geometría incorrecta")
    
    # Calcular sumatorias
    summation = SumTable(calc1, calc2, calc3)
    convection_results = ConvectionResults(summation, calcs, qmax)
    output_data = FinalValues(calcs, qmax, calc1, calc2, calc3, lamb, summation, convection_results)
    
    # Construir DataResult
    data_result = DataResult(
        thickness=output_data.thickness,
        thermal_diffusivity=output_data.thermal_diffusivity,
        conductivity_coefficient=output_data.conductivity_coefficient,
        convection_coefficient=output_data.convection_coefficient,
        initial_temperature=output_data.initial_temperature,
        ambient_temperature=output_data.ambient_temperature,
        density=output_data.density,
        specific_heat=output_data.specific_heat,
        distance=output_data.distance,
        time=output_data.time,
        iterations=output_data.iterations,
        biot=output_data.biot,
        geometry=output_data.geometry,
        q_max=output_data.q_max,
        calc1=CalculationResult(
            value_a=output_data.calc1.value_a,
            value_theta_o=output_data.calc1.value_theta_o,
            value_theta=output_data.calc1.value_theta,
            value_q=output_data.calc1.value_q,
        ),
        calc2=CalculationResult(
            value_a=output_data.calc2.value_a,
            value_theta_o=output_data.calc2.value_theta_o,
            value_theta=output_data.calc2.value_theta,
            value_q=output_data.calc2.value_q,
        ),
        calc3=CalculationResult(
            value_a=output_data.calc3.value_a,
            value_theta_o=output_data.calc3.value_theta_o,
            value_theta=output_data.calc3.value_theta,
            value_q=output_data.calc3.value_q,
        ),
        lamb=LambdaValues(
            lambda1=output_data.lambda_val.lambda1,
            lambda2=output_data.lambda_val.lambda2,
            lambda3=output_data.lambda_val.lambda3,
        ),
        value_a=output_data.value_a,
        value_theta_o=output_data.value_theta_o,
        value_theta=output_data.value_theta,
        value_q=output_data.value_q,
        tem=output_data.tem,
        q=output_data.q
    )

    return data_result
