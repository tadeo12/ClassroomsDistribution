import random
import math
from app.Logic.Evaluator import evaluate
from ConfigManager import ConfigManager

def generateNeighbor(allocation: dict):
    neighbor = allocation.copy()
    resources = list(neighbor.keys())
    A, B = random.sample(resources,2)
    neighbor[A], neighbor[B] =  neighbor[B], neighbor[A] 
    return neighbor 

def simulatedAnnealing(initialAllocation: dict, progressCallback = None):
    config = ConfigManager().getConfig()   
    trc = config["TEMPERATURE_REDUCTION_COEFFICIENT"]
    maxI = config["MAX_ITERATIONS"]
    solution = initialAllocation
    current = solution
    temperature=1
    i= 0
    currentCost = evaluate(initialAllocation)[0]
    solutionCost = currentCost

    if progressCallback:
        checkpoint = max(1, maxI // 100)

    while i < maxI and solutionCost > 0:
        #print(f"iteracion: {i}")
        i+=1
        neighbor = generateNeighbor(current)
        neighborEvaluation = evaluate(neighbor)
        difference = neighborEvaluation[0] - currentCost
        if difference < 0:
            current = neighbor
            solution= neighbor
            currentCost= neighborEvaluation[0]
            solutionCost= currentCost
        else:
            if math.exp(-difference/temperature) > random.random():
                current = neighbor
                currentCost=neighborEvaluation[0]
        temperature *= trc

        if progressCallback and i % checkpoint == 0:
            progressCallback(int((i/maxI)* 100), solutionCost)

    print("fin del algoritmo")
    return solution
