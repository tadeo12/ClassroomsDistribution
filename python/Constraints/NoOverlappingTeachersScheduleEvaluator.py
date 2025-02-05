from Constraints.BaseEvaluator import BaseEvaluator


class NoOverlappingTeachersScheduleEvaluator(BaseEvaluator):

    def evaluate(self, allocation):
        return 0