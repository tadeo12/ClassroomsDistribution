from collections import defaultdict
from Constraints.BaseEvaluator import BaseEvaluator


def groupByDayAndHour(allocation):
    resourcesByCommission = defaultdict(lambda: defaultdict(list))
    for resource, commission in allocation.items():
        resourcesByCommission[(resource.day,resource.hour)].append(commission)
    return resourcesByCommission

def countGroupsInBothCommissions(commissionA, commissionB):
    amount = 0
    for i in range(commissionA.groups):
        for j in range(commissionB.groups):
            if commissionA.groups[i] == commissionB.groups[j]:
                amount+= 1
    return amount

class NoOverlappingStudentsScheduleInPreferentialPlanEvaluator(BaseEvaluator):
    def evaluate(self, allocation):
        penalty = 0
        commissionsWithClassesAtTheSameTime = groupByDayAndHour(allocation)
        for (day,hour), commissions in commissionsWithClassesAtTheSameTime:
            for i in range(len(commissions)):
                for j in range(i+1,len(commissions)):
                    penalty += countGroupsInBothCommissions(commissions[i],commissions[j])
        return penalty