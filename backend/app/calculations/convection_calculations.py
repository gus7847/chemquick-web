import math
import numpy as np
import scipy.special as sp
import sympy as sy
from dataclasses import dataclass

@dataclass
class InitialCalcsData:
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

class InitialCalcs:
    """
    A class to perform initial calculations based on a set of initial values.

    Attributes:
        characteristic_length (float): The characteristic length calculated as half the thickness.
        dimensionless_distance (float): Dimensionless distance calculated as distance divided by the characteristic length.
        dimensionless_time (float): Dimensionless time calculated as time times thermal diffusivity divided by the square of the characteristic length.
        thickness (float): Thickness of the material.
        thermal_diffusivity (float): Thermal diffusivity of the material.
        conductivity_coefficient (float): Conductivity coefficient of the material.
        convection_coefficient (float): Convection coefficient of the material.
        initial_temperature (float): Initial temperature of the material.
        ambient_temperature (float): Ambient temperature.
        density (float): Density of the material.
        specific_heat (float): Specific heat capacity of the material.
        distance (float): Distance for calculation.
        time (float): Time for calculation.

    Methods:
        __init__(self, initial_parameters): Initializes the InitialCalcs object with a list of initial values.
    """

    def __init__(self, initial_parameters):
        # thickness, thermal_diffusivity, conductivity_coefficient, convection_coefficient, initial_temperature, ambient_temperature, density, specific_heat, distance, time, iterations, biot, geometry = initial_parameters
        self.thickness = initial_parameters.thickness
        self.thermal_diffusivity = initial_parameters.thermal_diffusivity
        self.conductivity_coefficient = initial_parameters.conductivity_coefficient
        self.convection_coefficient = initial_parameters.convection_coefficient
        self.initial_temperature = initial_parameters.initial_temperature
        self.ambient_temperature = initial_parameters.ambient_temperature
        self.density = initial_parameters.density
        self.specific_heat = initial_parameters.specific_heat
        self.distance = initial_parameters.distance
        self.time = initial_parameters.time
        self.iterations = initial_parameters.iterations
        self.biot = initial_parameters.biot
        self.geometry = initial_parameters.geometry
        characteristic_length = self.thickness / 2
        self.characteristic_length = characteristic_length

        dimensionless_distance = self.distance / characteristic_length
        self.dimensionless_distance = dimensionless_distance

        dimensionless_time = (self.time * self.thermal_diffusivity) / \
            (characteristic_length ** 2)
        self.dimensionless_time = dimensionless_time


def calc_qmax(calc_values, control):
    """
    Calculates the maximum heat transfer rate (q_max) for different geometries.

    Parameters:
        calc_values (InitialCalcs): An instance of InitialCalcs containing material and geometric properties.
        control (str): The type of geometry for which to calculate q_max. Options are 'plate', 'cylinder', 'sphere'.

    Returns:
        float: The calculated maximum heat transfer rate (q_max).
    """
    if (control == 'plate'):
        q_max = calc_values.thickness * calc_values.density * \
            calc_values.specific_heat * (calc_values.ambient_temperature - calc_values.initial_temperature)
    elif (control == 'cylinder'):
        q_max = calc_values.density * calc_values.specific_heat * math.pi * \
            (calc_values.characteristic_length ** 2) * \
            (calc_values.ambient_temperature - calc_values.initial_temperature)
    elif (control == 'sphere'):
        q_max = calc_values.density * calc_values.specific_heat * (4 / 3) * math.pi * (
            calc_values.characteristic_length ** 3) * (calc_values.ambient_temperature - calc_values.initial_temperature)

    return q_max


def calc_alpha(calc_values):
    """
    Calculates the thermal diffusivity (alpha) of the material.

    Parameters:
        calc_values (InitialCalcs): An instance of InitialCalcs containing material and geometric properties.

    Returns:
        float: The calculated thermal diffusivity (alpha).
    """
    alpha = calc_values.conductivity_coefficient / \
        (calc_values.density * calc_values.specific_heat)
    return alpha


def calc_biot(calc_values):
    """
    Calculates the Biot number (Bi) for the material.

    Parameters:
        calc_values (InitialCalcs): An instance of InitialCalcs containing material and geometric properties.

    Returns:
        float: The calculated Biot number (Bi).
    """
    biot = calc_values.convection_coefficient * \
        calc_values.characteristic_length / calc_values.conductivity_coefficient
    return biot

def calc_alpha(calc_values):
    """
    Calculates the thermal diffusivity (alpha) of the material.

    Parameters:
        calc_values (InitialCalcs): An instance of InitialCalcs containing material and geometric properties.

    Returns:
        float: The calculated thermal diffusivity (alpha).
    """
    alpha = calc_values.conductivity_coefficient / (calc_values.density * calc_values.specific_heat)
    return alpha


class LambdaPlate:
    """
    A class for calculating the lambda values in the context of thermal analysis for a plate.

    This class calculates three lambda values based on the Biot number and a specified number of iterations. These lambda values are crucial for solving heat transfer problems in plates, especially when dealing with transient heat conduction.

    Attributes:
        lambda1 (float): The first lambda value calculated using the Biot number and iterative approach.
        lambda2 (float): The second lambda value, incorporating an additional pi to the iterative calculation.
        lambda3 (float): The third lambda value, incorporating an additional 2*pi to the iterative calculation.

    Parameters:
        biot (float): The Biot number, a dimensionless number important in heat transfer calculations.
        n (int): The number of iterations to use in the calculation of lambda values.

    Methods:
        __init__(self, biot, n):
            Initializes the LambdaPlate object by calculating lambda1, lambda2, and lambda3 based on the provided Biot number and number of iterations.
    """

    def __init__(self, biot, n):
        lambda_val = 1
        for i in range(n):
            lambda_new = math.atan(biot / lambda_val)
            lambda_val = lambda_new
        self.lambda1 = lambda_val

        lambda_val = 1
        for i in range(n):
            lambda_new = math.atan(biot / lambda_val) + math.pi
            lambda_val = lambda_new
        self.lambda2 = lambda_val

        lambda_val = 1
        for i in range(n):
            lambda_new = math.atan(biot / lambda_val) + (2 * math.pi)
            lambda_val = lambda_new
        self.lambda3 = lambda_val
    
    def to_dict(self):
        return {
            'lambda1': self.lambda1,
            'lambda2': self.lambda2,
            'lambda3': self.lambda3
        }


class LambdaCylinder:
    """
    A class for calculating the lambda values for a cylindrical geometry in thermal analysis.

    This class calculates three lambda values based on the Biot number and a specified number of iterations. These lambda values are essential for analyzing heat transfer in cylindrical objects, particularly in the context of transient heat conduction problems.

    The calculation uses the properties of Bessel functions, which are crucial in the thermal analysis of cylindrical geometries. The iterative method refines the lambda values to achieve a more accurate solution.

    Attributes:
        lambda1 (float): The first lambda value, starting from an initial guess of 1.
        lambda2 (float): The second lambda value, starting from an initial guess of 4.
        lambda3 (float): The third lambda value, starting from an initial guess of 8.

    Parameters:
        biot (float): The Biot number, a dimensionless number representing the ratio of conductive to convective heat transfer rates across a boundary.
        n (int): The number of iterations to refine the lambda values.

    Methods:
        __init__(self, biot, n):
            Initializes the LambdaCylinder object by calculating lambda1, lambda2, and lambda3 based on the provided Biot number and number of iterations.
    """

    def __init__(self, biot, n):
        lambda_val = 1
        for i in range(n):
            lambda_new = lambda_val - (lambda_val * sp.jv(1, lambda_val) - biot * sp.jv(
                0, lambda_val)) / (lambda_val * sp.jv(0, lambda_val) + biot * sp.jv(1, lambda_val))
            lambda_val = lambda_new
        self.lambda1 = lambda_val

        lambda_val = 4
        for i in range(n):
            lambda_new = lambda_val - (lambda_val * sp.jv(1, lambda_val) - biot * sp.jv(
                0, lambda_val)) / (lambda_val * sp.jv(0, lambda_val) + biot * sp.jv(1, lambda_val))
            lambda_val = lambda_new
        self.lambda2 = lambda_val

        lambda_val = 8
        for i in range(n):
            lambda_new = lambda_val - (lambda_val * sp.jv(1, lambda_val) - biot * sp.jv(
                0, lambda_val)) / (lambda_val * sp.jv(0, lambda_val) + biot * sp.jv(1, lambda_val))
            lambda_val = lambda_new
        self.lambda3 = lambda_val

        print("Lambda1 Cilindro: ", self.lambda1)
        print("Lambda2: ", self.lambda2)
        print("Lambda3: ", self.lambda3)

    def to_dict(self):
        return {
            'lambda1': self.lambda1,
            'lambda2': self.lambda2,
            'lambda3': self.lambda3
        }


class LambdaSphere:
    """
    A class for calculating the lambda values for a spherical geometry in thermal analysis.

    This class calculates three lambda values based on the Biot number and a specified number of iterations. These lambda values are crucial for solving heat transfer problems in spherical objects, especially in the context of transient heat conduction.

    The iterative method used for calculation adjusts the lambda values based on the inverse cotangent function, reflecting the unique thermal properties and challenges associated with spherical geometries.

    Attributes:
        lambda1 (float): The first lambda value, refined through iterations starting from an initial guess.
        lambda2 (float): The second lambda value, incorporating an additional pi to the iterative calculation for phase adjustment.
        lambda3 (float): The third lambda value, incorporating an additional 2*pi for further phase adjustment.

    Parameters:
        biot (float): The Biot number, a dimensionless number important in heat transfer calculations, representing the ratio of conductive to convective heat transfer rates across a boundary.
        n (int): The number of iterations to use in the calculation of lambda values.

    Methods:
        __init__(self, biot, n):
            Initializes the LambdaSphere object by calculating lambda1, lambda2, and lambda3 based on the provided Biot number and number of iterations.
    """
    
    def __init__(self, biot, n):
        lambda_val = 1
        for i in range(n):
            lambda_new = sy.acot((1 - biot) / lambda_val)
            lambda_val = lambda_new
        self.lambda1 = np.float64(lambda_val) # Convert to float64 to avoid JSON serialization issues

        lambda_val = 1
        for i in range(n):
            lambda_new = sy.acot((1 - biot) / lambda_val) + math.pi
            lambda_val = lambda_new
        self.lambda2 = np.float64(lambda_val) # Convert to float64 to avoid JSON serialization issues

        lambda_val = 1
        for i in range(n):
            lambda_new = sy.acot((1 - biot) / lambda_val) + (2 * math.pi)
            lambda_val = lambda_new
        self.lambda3 = np.float64(lambda_val) # Convert to float64 to avoid JSON serialization issues
    
    def to_dict(self):
        return {
            'lambda1': self.lambda1,
            'lambda2': self.lambda2,
            'lambda3': self.lambda3
        }


class Plate:
    """
    A class for calculating various thermal properties of a plate based on given lambda values and calculated values.

    This class computes specific thermal properties such as the amplitude factor (a), the initial temperature distribution (theta_o), the temperature distribution at a given time and position (theta), and the heat flux (q) for a plate. These calculations are essential for understanding the thermal behavior of the plate under given conditions.

    Attributes:
        value_a (float): The amplitude factor 'a', calculated based on the lambda value.
        value_theta_o (float): The initial temperature distribution 'theta_o', calculated using the amplitude factor and the exponential decay of temperature over time.
        value_theta (float): The temperature distribution 'theta' at a given time and position, calculated using the initial temperature distribution and the cosine of the product of lambda value and dimensionless distance.
        value_q (float): The heat flux 'q', calculated using the initial temperature distribution and the sine of lambda value divided by lambda value itself.

    Parameters:
        calc_values (CalculatedValues): An object of CalculatedValues class containing the dimensionless time and distance used in the calculations.
        lambda_val (float): The lambda value used in the calculations, typically determined from the solution of the characteristic equation for the plate.

    Methods:
        __init__(self, calc_values, lambda_val):
            Initializes the Plate object with calculated thermal properties based on the provided lambda value and calculated values object.
    """

    def __init__(self, calc_values, lambda_val):
        lambda_a = (4 * math.sin(lambda_val)) / \
            (2 * lambda_val + math.sin(2 * lambda_val))
        self.value_a = lambda_a

        lambda_theta_o = lambda_a * \
            math.exp(-(lambda_val ** 2 * calc_values.dimensionless_time))
        self.value_theta_o = lambda_theta_o

        lambda_theta = lambda_theta_o * \
            math.cos(lambda_val * calc_values.dimensionless_distance)
        self.value_theta = lambda_theta

        lambda_q = (lambda_theta_o * math.sin(lambda_val)) / lambda_val
        self.value_q = lambda_q

    def to_dict(self):
        return {
            'value_a': self.value_a,
            'value_theta_o': self.value_theta_o,
            'value_theta': self.value_theta,
            'value_q': self.value_q
        }


class Cylinder:
    """
    A class for calculating various thermal properties of a cylinder based on given lambda values and calculated values.

    This class computes specific thermal properties such as the amplitude factor (a), the initial temperature distribution (theta_o), the temperature distribution at a given time and position (theta), and the heat flux (q) for a cylinder. These calculations are essential for understanding the thermal behavior of the cylinder under given conditions.

    The calculations utilize Bessel functions, reflecting the cylindrical geometry's influence on the heat transfer process.

    Attributes:
        value_a (float): The amplitude factor 'a', calculated based on the lambda value and Bessel functions.
        value_theta_o (float): The initial temperature distribution 'theta_o', calculated using the amplitude factor and the exponential decay of temperature over time.
        value_theta (float): The temperature distribution 'theta' at a given time and position, calculated using the initial temperature distribution and the Bessel function of the first kind.
        value_q (float): The heat flux 'q', calculated using the initial temperature distribution and the derivative of the Bessel function of the first kind.

    Parameters:
        calc_values (CalculatedValues): An object of CalculatedValues class containing the dimensionless time and distance used in the calculations.
        lambda_val (float): The lambda value used in the calculations, typically determined from the solution of the characteristic equation for the cylinder.

    Methods:
        __init__(self, calc_values, lambda_val):
            Initializes the Cylinder object with calculated thermal properties based on the provided lambda value and calculated values object.
    """

    def __init__(self, calc_values, lambda_val):
        lambda_a = (2 / lambda_val) * sp.jv(1, lambda_val) / (sp.jv(0, lambda_val) ** 2 + sp.jv(1, lambda_val) ** 2)
        self.value_a = np.float64(lambda_a)
        print(lambda_a, "aaa")

        lambda_theta_o = lambda_a * math.exp(-(lambda_val ** 2 * calc_values.dimensionless_time))
        self.value_theta_o = np.float64(lambda_theta_o)
        print(lambda_theta_o, "ooo")

        lambda_theta = lambda_theta_o * sp.jv(0, lambda_val * calc_values.dimensionless_distance)
        self.value_theta = np.float64(lambda_theta)
        print(lambda_theta, "tttt")

        lambda_q = 2 * lambda_theta_o * sp.jv(1, lambda_val) / lambda_val
        self.value_q = np.float64(lambda_q)
        print(lambda_q, "qqqq")
    
    def to_dict(self):
        return {
            'value_a': self.value_a,
            'value_theta_o': self.value_theta_o,
            'value_theta': self.value_theta,
            'value_q': self.value_q
        }



class Sphere:
    """
    A class for calculating various thermal properties of a sphere based on given lambda values and calculated values.

    This class computes specific thermal properties such as the amplitude factor (a), the initial temperature distribution (theta_o), the temperature distribution at a given time and position (theta), and the heat flux (q) for a sphere. These calculations are essential for understanding the thermal behavior of the sphere under given conditions.

    The calculations are based on spherical coordinates and take into account the unique aspects of heat transfer in spherical geometries, such as the distribution of temperature and heat flux over the sphere's surface.

    Attributes:
        value_a (float): The amplitude factor 'a', calculated based on the lambda value and its trigonometric functions, representing the initial amplitude of temperature variation.
        value_theta_o (float): The initial temperature distribution 'theta_o', calculated using the amplitude factor and the exponential decay of temperature over time.
        value_theta (float): The temperature distribution 'theta' at a given time and position, calculated using the initial temperature distribution and the sine of lambda value times the dimensionless distance, divided by the product of lambda value and dimensionless distance.
        value_q (float): The heat flux 'q', calculated using the initial temperature distribution and the trigonometric functions of lambda value, representing the rate of heat transfer per unit area.

    Parameters:
        calc_values (CalculatedValues): An object of CalculatedValues class containing the dimensionless time and distance used in the calculations.
        lambda_val (float): The lambda value used in the calculations, typically determined from the solution of the characteristic equation for the sphere.

    Methods:
        __init__(self, calc_values, lambda_val):
            Initializes the Sphere object with calculated thermal properties based on the provided lambda value and calculated values object.
    """

    def __init__(self, calc_values, lambda_val):
        lambda_a = 4 * (math.sin(lambda_val) - lambda_val * math.cos(lambda_val)
                        ) / (2 * lambda_val - math.sin(2 * lambda_val))
        self.value_a = np.float64(lambda_a)

        lambda_theta_o = lambda_a * \
            math.exp(-(lambda_val ** 2 * calc_values.dimensionless_time))
        self.value_theta_o = np.float64(lambda_theta_o)

        if(calc_values.dimensionless_distance == 0):
            parte_espacial = 1
        else:
            parte_espacial = math.sin(lambda_val * calc_values.dimensionless_distance) / (lambda_val * calc_values.dimensionless_distance)

        lambda_theta = lambda_theta_o * parte_espacial

        self.value_theta = np.float64(lambda_theta)

        lambda_q = 3 * lambda_theta_o * \
            (math.sin(lambda_val) - lambda_val *
             math.cos(lambda_val)) / lambda_val ** 3
        self.value_q = np.float64(lambda_q)

    def to_dict(self):
        return {
            'value_a': self.value_a,
            'value_theta_o': self.value_theta_o,
            'value_theta': self.value_theta,
            'value_q': self.value_q
        }



class SumTable:
    """
    SumTable class to calculate the summation of values from three objects.

    This class takes three objects that are expected to have the attributes value_a, value_theta_o,
    value_theta, and value_q. It calculates the summation of these values for each attribute and
    stores them as attributes of the SumTable instance.

    Attributes:
        summation_a (float): Summation of the 'value_a' values from the three objects.
        summation_theta_o (float): Summation of the 'value_theta_o' values from the three objects.
        summation_theta (float): Summation of the 'value_theta' values from the three objects.
        summation_q (float): Summation of the 'value_q' values from the three objects.

    Args:
        lambda_1: The first object with the attributes value_a, value_theta_o         value_theta, and value_q.
        lambda_2: The second object with the attributes value_a, value_theta_o, value_theta, and value_q.
        lambda_3: The third object with the attributes value_a, value_theta_o, value_theta, and value_q.
    """

    def __init__(self, lambda_1, lambda_2, lambda_3):
        summation_a = lambda_1.value_a + lambda_2.value_a + lambda_3.value_a
        self.summation_a = summation_a

        summation_theta_o = lambda_1.value_theta_o + \
            lambda_2.value_theta_o + lambda_3.value_theta_o
        self.summation_theta_o = summation_theta_o

        summation_theta = lambda_1.value_theta + \
            lambda_2.value_theta + lambda_3.value_theta
        self.summation_theta = summation_theta

        summation_q = lambda_1.value_q + lambda_2.value_q + lambda_3.value_q
        self.summation_q = summation_q
        print(summation_a, summation_theta_o, summation_theta, summation_q)

class ConvectionResults:
    """
    ConvectionResults class to calculate and store convection results.

    This class takes the summation results object, previously calculated values,
    and the maximum heat flux value to calculate the mean surface temperature (tem)
    and the heat flux (q) under convection conditions.

    Attributes:
        tem (float): Mean surface temperature calculated from the summation results and calculated values.
        q (float): Heat flux calculated from the maximum heat flux and the summation results.

    Args:
        summation_results: Object that contains the summation results (should have attributes summation_theta and summation_q).
        calc_values: Object that contains previously calculated values (should have attributes initial_temperature and ambient_temperature).
        q_max (float): Maximum heat flux value.
    """

    #Cambiar Tem a T(x, t) para placa y T(r, t) para cilindro y esfera
    def __init__(self, summation_results, calc_values, q_max):
        tem = summation_results.summation_theta * \
            (calc_values.initial_temperature - calc_values.ambient_temperature) + calc_values.ambient_temperature
        self.tem = tem

        q = (1 - summation_results.summation_q) * q_max
        self.q = q


class FinalValues:
    """
    Class for storing and managing the final calculated values.

    Attributes:
        thickness (float): Thickness of the material.
        thermal_diffusivity (float): Thermal diffusivity of the material.
        conductivity_coefficient (float): Conductivity coefficient of the material.
        convection_coefficient (float): Convection coefficient of the material.
        initial_temperature (float): Initial temperature of the material.
        ambient_temperature (float): Ambient temperature.
        density (float): Density of the material.
        specific_heat (float): Specific heat capacity of the material.
        distance (float): Distance considered for the calculation.
        time (float): Total analysis time.
        iterations (int): Number of iterations performed.
        biot (float): Biot number of the analysis.
        geometry (str): Geometry of the analyzed object.
        q_max (float): Maximum heat flux.
        calc1, calc2, calc3 (float): Intermediate calculation results.
        lambda (float): Lambda value used in the calculations.
        value_a (float): Summation of 'a' calculated.
        value_theta_o (float): Summation of initial theta calculated.
        value_theta (float): Summation of theta calculated.
        value_q (float): Summation of heat flux calculated.
        tem (float): Final temperature calculated.
        q (float): Final heat flux calculated.

    Parameters:
        calcs (obj): Object containing the initial calculations and attributes.
        q_max (float): Maximum heat flux.
        calc1, calc2, calc3 (float): Intermediate calculation results.
        lambda_val (float): Lambda value used in the calculations.
        summation (obj): Object containing the calculated summations.
        results (obj): Object containing the final temperature and heat flux results.
    """

    def __init__(self, calcs, q_max, calc1, calc2, calc3, lambda_val, summation, results):
        self.thickness = calcs.thickness
        self.thermal_diffusivity = calcs.thermal_diffusivity
        self.conductivity_coefficient = calcs.conductivity_coefficient
        self.convection_coefficient = calcs.convection_coefficient
        self.initial_temperature = calcs.initial_temperature
        self.ambient_temperature = calcs.ambient_temperature
        self.density = calcs.density
        self.specific_heat = calcs.specific_heat
        self.distance = calcs.distance
        self.time = calcs.time
        self.iterations = calcs.iterations
        self.biot = calcs.biot
        self.geometry = calcs.geometry
        self.q_max = q_max
        self.calc1 = calc1
        self.calc2 = calc2
        self.calc3 = calc3
        self.lambda_val = lambda_val
        self.value_a = summation.summation_a
        self.value_theta_o = summation.summation_theta_o
        self.value_theta = summation.summation_theta
        self.value_q = summation.summation_q
        self.tem = results.tem
        self.q = results.q

    def to_dict(self):
        return {
            'thickness': self.thickness,
            'thermal_diffusivity': self.thermal_diffusivity,
            'conductivity_coefficient': self.conductivity_coefficient,
            'convection_coefficient': self.convection_coefficient,
            'initial_temperature': self.initial_temperature,
            'ambient_temperature': self.ambient_temperature,
            'density': self.density,
            'specific_heat': self.specific_heat,
            'distance': self.distance,
            'time': self.time,
            'iterations': self.iterations,
            'biot': self.biot,
            'geometry': self.geometry,
            'q_max': self.q_max,
            'calc1': self.calc1.to_dict(),
            'calc2': self.calc2.to_dict(),
            'calc3': self.calc3.to_dict(),
            'lambda_val': self.lambda_val.to_dict(),
            'value_a': self.value_a,
            'value_theta_o': self.value_theta_o,
            'value_theta': self.value_theta,
            'value_q': self.value_q,
            'tem': self.tem,
            'q': self.q
        }
