from collections import defaultdict
from Constraints.BaseEvaluator import BaseEvaluator


def groupByDayHourAndTeacher(allocation):
    resourcesByDayHourAndTeacher = defaultdict(list)
    for resource, commission in allocation.items():
        resourcesByDayHourAndTeacher[(resource.day,resource.hour,commission.teacher)].append(commission)
    return resourcesByDayHourAndTeacher

class NoOverlappingTeachersScheduleEvaluator(BaseEvaluator):

    def evaluate(self, allocation):
        resourcesByDayHourAndTeacher= resourcesByDayHourAndTeacher(allocation)
        penalty = 0
        for resources in resourcesByDayHourAndTeacher:
            if len(resources)>1:
                #si es el mismo aula, es la misma clase pero para dos materias en simultadeo, lo que no se deberia penalizar
                for i in range(len(resources)):
                    for j in range(i+1,len(resources)):
                        if resources[i].classroom != resources[j].classroom:
                            penalty+= 1
        return penalty