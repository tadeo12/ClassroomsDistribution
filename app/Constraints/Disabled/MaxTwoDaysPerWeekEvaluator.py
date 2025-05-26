from Constraints.BaseEvaluator import BaseEvaluator
from collections import defaultdict



def groupByCommission(allocation):
        resourcesByCommission = defaultdict(list)
        for resource, commission in allocation.items():
            resourcesByCommission[commission].append(resource)
        return resourcesByCommission

class MaxTwoDaysPerWeekEvaluator(BaseEvaluator):

    def evaluate(self, allocation):
        resourcesByCommission= groupByCommission(allocation)
        penalty = 0
        for commission, resources in resourcesByCommission.items() :
            days = set()
            for resource in resources:
                days.add(resource.day)
            penalty += len(days) - 2 
        return penalty