from collections import defaultdict
from app.Constraints.BaseEvaluator import BaseEvaluator
from ConfigManager import ConfigManager

def groupByCommissionAndDay(allocation):
        resourcesByDayAndCommission = defaultdict(lambda: defaultdict(list))
        for resource, commission in allocation.items():
            resourcesByDayAndCommission[commission][resource.day].append(resource)
        return resourcesByDayAndCommission

class DayOffBetweenClassesEvaluator(BaseEvaluator):

    def evaluate(self, allocation):
        resourcesByCommissionsAndDay = groupByCommissionAndDay(allocation)
        penalty= 0
        daysPerWeek = ConfigManager().getConfig()["DAYS_PER_WEEK"]
        for commission, resourcesByDay in resourcesByCommissionsAndDay.items():
            prevDayWereClasses = bool(resourcesByDay[0])
            for i in range(1, daysPerWeek):
                if prevDayWereClasses and resourcesByDay[i]:
                    penalty+=1
                prevDayWereClasses = bool(resourcesByDay[i])
        return penalty