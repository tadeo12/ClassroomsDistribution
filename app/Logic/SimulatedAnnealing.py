import random
import math
from app.Models import *
from app.Logic.Evaluator import evaluate
from ConfigurationVars import *


def generateNeighbor(allocation: dict):
    neighbor = allocation.copy()
    resources = list(neighbor.keys())
    A, B = random.sample(resources,2)
    neighbor[A], neighbor[B] =  neighbor[B], neighbor[A] 
    return neighbor 


def simulatedAnnealing(initialAllocation: dict):
    solution = initialAllocation
    current = solution
    trc = TEMPERATURE_REDUCTION_COEFFICIENT
    temperature=1
    i= 0
    currentCost = evaluate(initialAllocation)[0]
    solutionCost = currentCost
    while i < MAX_ITERATIONS and solutionCost > 0:
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
    return solution
