from ConfigManager import ConfigManager  
import math

def cool(t: float, iteration: int ) -> float:
    config = ConfigManager().getConfig()
    method = config.get("cooling_function", "geometric")

    if method == "geometric":
        coeff = config.get("temperature_reduction_coefficient", 0.9)
        return t * coeff

    elif method == "rational":
        beta = config.get("temperature_beta_constant", 0.01)
        return t / (1 + beta * t)

    elif method == "logarithmic":
        c = config.get("temperature_log_c", 0.1)  # constante para ajustar la velocidad
        ti = config.get("initial_temperature", 1)
        # evitamos log(0) arrancando en k>=1
        return ti / (1 + c * math.log(1 + iteration))

    else:
        raise ValueError(f"Unknown cooling function: {method}")