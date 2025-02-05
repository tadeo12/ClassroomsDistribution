from Constraints.BaseEvaluator import BaseEvaluator


class DayOffBetweenClassesEvaluator(BaseEvaluator):

    def evaluate(self, allocation):
        return 0