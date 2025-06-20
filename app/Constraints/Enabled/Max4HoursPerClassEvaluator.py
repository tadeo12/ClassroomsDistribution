from app.Constraints.BaseEvaluator import BaseEvaluator
from collections import defaultdict

from ConfigurationVars import HOURS_PER_RESOURCE


def groupByDayAndCommission(allocation):
        resourcesByDayAndCommission = defaultdict(lambda: defaultdict(list))
        for resource, commission in allocation.items():
            resourcesByDayAndCommission[resource.day][commission].append(resource)
        return resourcesByDayAndCommission

class Max4HoursPerClassEvaluator(BaseEvaluator):
    def evaluate(self, allocation):
        maxResources = int(4 / HOURS_PER_RESOURCE) 
        penalty = 0
        resourcesByDayAndCommission = groupByDayAndCommission(allocation)
        for day, commissions in resourcesByDayAndCommission.items():
            for commission, resources in commissions.items():
                sortedResources=sorted(resources,key=lambda r: r.hour)
                countFollowedResources = 1
                prevHour = sortedResources[0].hour
                for resource in sortedResources[1:]:
                    if resource.hour == prevHour + 1:
                        countFollowedResources += 1
                    else:
                        countFollowedResources = 1
                    prevHour = resource.hour
                    if countFollowedResources > maxResources:
                        penalty += 1
        return penalty