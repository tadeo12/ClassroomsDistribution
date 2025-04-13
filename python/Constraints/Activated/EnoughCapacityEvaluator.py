from Constraints.BaseEvaluator import BaseEvaluator

class EnoughCapacityEvaluator(BaseEvaluator):
    def evaluate(self, allocation):
        penalty = 0
        for resource, commission in allocation.items():
            penalty += max(0, commission.students - resource.classroom.capacity)
        return penalty