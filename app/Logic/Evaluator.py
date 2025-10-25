import logging
from app.Logic.ConstraintLoader import load_evaluator_classes
from ConfigManager import ConfigManager
from app.Logic.PenaltyWeights import weights

# Cache para clases y sus valores máximos
_classesCache = None


def _getClasses():
    """Carga y cachea las clases de evaluadores junto con sus valores máximos."""
    global _classesCache
    if _classesCache is not None:
        return _classesCache

    evaluator_classes = load_evaluator_classes()
    _classesCache = {}

    for name, evaluatorClass in evaluator_classes.items():
        try:
            instance = evaluatorClass()
            max_value = None
            max_happy = None

            # Calcular los valores máximos una sola vez
            if hasattr(instance, "maxValue") and callable(instance.maxValue):
                try:
                    max_value = instance.maxValue()
                    
                except Exception as e:
                    logging.warning(f"Error al calcular maxValue() de {name}: {e}")

            if hasattr(instance, "maxHappyValue") and callable(instance.maxHappyValue):
                try:
                    max_happy = instance.maxHappyValue()
                except Exception as e:
                    logging.warning(f"Error al calcular maxHappyValue() de {name}: {e}")

            _classesCache[name] = {
                "class": evaluatorClass,
                "maxValue": max_value,
                "maxHappyValue": max_happy,
            }

            logging.debug(
                f"Cargado {name} con maxValue={max_value}, maxHappyValue={max_happy}"
            )

        except Exception as e:
            logging.error(f"Error al inicializar la clase {name}: {e}")

    return _classesCache


def summatoryEvaluation(allocation: dict):
    """Evalúa la suma simple de todas las penalizaciones."""
    totalCost = 0
    constraintsEvaluations = {}

    for name, data in _getClasses().items():
        evaluator = data["class"]()
        cost = evaluator.evaluate(allocation)

        if cost is not None:
            totalCost += cost
            constraintsEvaluations[name] = cost
        else:
            logging.error(f"Error al calcular la penalización de {name}")
            constraintsEvaluations[name] = None

    return totalCost, constraintsEvaluations


def fixedWeightedPenaltyEvaluation(allocation: dict):
    """Evalúa penalizaciones ponderadas por pesos fijos."""
    totalCost = 0
    constraintsEvaluations = {}

    for name, data in _getClasses().items():
        evaluator = data["class"]()
        cost = evaluator.evaluate(allocation)
        weight = weights.get(name)

        if cost is None:
            logging.error(f"Error al calcular la penalización de {name}")
            raise ValueError(f"Cost es None para {name}")
        if weight is None:
            logging.error(f"Error al cargar el peso de la penalización de {name}")
            raise ValueError(f"Peso no definido para {name}")

        totalCost += weight * cost
        constraintsEvaluations[name] = cost

    return totalCost, constraintsEvaluations


def normalizedPenaltyEvaluation(allocation: dict, use_happy=False):
    """
    Evalúa penalizaciones normalizadas y ponderadas por su peso.
    Usa maxValue o maxHappyValue (si use_happy=True).
    En el modo 'feliz', el valor normalizado se trunca a 1.
    """
    totalCost = 0
    constraintsEvaluations = {}

    for name, data in _getClasses().items():
        evaluator = data["class"]()
        cost = evaluator.evaluate(allocation)
        weight = weights.get(name)

        if cost is None:
            logging.error(f"Error al calcular la penalización de {name}")
            continue
        if weight is None:
            logging.error(f"Error al cargar el peso de la penalización de {name}")
            raise ValueError(f"Peso no definido para {name}")

        max_value = data["maxHappyValue"] if use_happy else data["maxValue"]

        if max_value is None or max_value == 0:
            #logging.warning(
            #    f"No se pudo obtener valor máximo para {name} — se usará el valor sin normalizar."
            #)
            normalized_cost = cost
        else:
            normalized_cost = cost / max_value
            if use_happy:
                normalized_cost = min(normalized_cost, 1)

        weighted_cost = weight * normalized_cost
        totalCost += weighted_cost

        constraintsEvaluations[name] = {
            "raw": cost,
            "max": max_value,
            "normalized": normalized_cost,
            "weighted": weighted_cost,
            "weight": weight,
        }

    return totalCost, constraintsEvaluations


def evaluate(allocation: dict):
    """Selecciona el método de evaluación según la configuración."""
    config = ConfigManager().getConfig().get("penalty_function", "fwp")

    match config:
        case "sum":
            return summatoryEvaluation(allocation)
        case "fwp":
            return fixedWeightedPenaltyEvaluation(allocation)
        case "norm":
            return normalizedPenaltyEvaluation(allocation, use_happy=False)
        case "happy_norm":
            return normalizedPenaltyEvaluation(allocation, use_happy=True)
        case _:
            logging.warning(
                f"Función de penalización desconocida: {config}. Se usará 'fwp'."
            )
            return fixedWeightedPenaltyEvaluation(allocation)
