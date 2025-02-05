from Constraints.BaseEvaluator import BaseEvaluator


class NoOverlappingStudentsScheduleInPreferentialPlanEvaluator(BaseEvaluator):

    def evaluate(self, allocation):
        return 0