import logging
from app.Logic.ConstraintLoader import load_evaluation_functions
from ConfigManager import ConfigManager
from app.Logic.PenaltyWeights import weights

_functionsCache = None

def _getFunctions():
    global _functionsCache
    if _functionsCache is None:
        _functionsCache = load_evaluation_functions()
    return _functionsCache

def summmatoryEvaluation(allocation: dict):
    totalCost=0
    info = ""
    for function, evaluatorClass in _getFunctions().items():
        cost=evaluatorClass().evaluate(allocation)
        info += f"penalizacion de '{function}' : {cost}\n"
        if cost is not None:
            totalCost +=  cost
        else:
            logging.error(f"Error al calcular la penalizacion de {function}")
    return totalCost, info
    

def fixedWeightedPenaltyEvaluation(allocation):
    totalCost = 0
    info = ""
    for function, evaluatorClass in _getFunctions().items():
        cost = evaluatorClass().evaluate(allocation)
        weight = weights.get(function)

        if cost is None:
            logging.error(f"Error al calcular la penalización de {function}")
            raise ValueError(f"Cost es None para {function}")
        if weight is None:
            logging.error(f"Error al cargar el peso de la penalización de {function}")
            raise ValueError(f"Peso no definido para {function}")
        
        info += f"penalización de '{function}' : {cost}\n"
        totalCost += weight * cost

    return totalCost, info


def evaluate(allocation: dict):
    #print("evaluando")
    match ConfigManager().getConfig()["PENALTY_FUNCTION"]:
        case "sum":
            return summmatoryEvaluation(allocation)
        case "fwp":
            return fixedWeightedPenaltyEvaluation(allocation)
        case _:
            return fixedWeightedPenaltyEvaluation(allocation)


    
