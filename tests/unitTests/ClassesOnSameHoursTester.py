import unittest
from app.Constraints.Enabled.ClassesOnSameHoursEvaluator import ClassesOnSameHoursEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *

class TestClassesOnSameHoursEvaluator(unittest.TestCase):
    def test_no_penalty_with_same_hours_on_all_days(self):
        evaluator = ClassesOnSameHoursEvaluator()
        commission = Commission("commission1", Teacher("teacher1"), Subject("subject"), students=10, hoursPerWeek=4)
        classroom = Classroom("classroom", 30, Place("place"))
        allocation = {
            Resource(classroom, day=0, hour=8): commission,
            Resource(classroom, day=0, hour=9): commission,
            Resource(classroom, day=2, hour=8): commission,
            Resource(classroom, day=2, hour=9): commission,
        }
        penalty = evaluator.evaluate(allocation)
        assert penalty == 0

    def test_penalty_with_different_hours_between_days(self):
        evaluator = ClassesOnSameHoursEvaluator()
        commission = Commission("commission1", Teacher("teacher1"), Subject("subject"), students=10, hoursPerWeek=4)
        classroom = Classroom("classroom", 30, Place("place"))
        allocation = {
            Resource(classroom, day=0, hour=8): commission,
            Resource(classroom, day=0, hour=9): commission,
            Resource(classroom, day=2, hour=10): commission,
            Resource(classroom, day=2, hour=11): commission,
        }
        penalty = evaluator.evaluate(allocation)
        assert penalty > 0

    def test_no_penalty_when_one_day_is_subset_of_other(self):
        evaluator = ClassesOnSameHoursEvaluator()
        commission = Commission("commission1", Teacher("teacher1"), Subject("subject"), students=10, hoursPerWeek=4)
        classroom = Classroom("classroom", 30, Place("place"))
        allocation = {
            Resource(classroom, day=0, hour=8): commission,
            Resource(classroom, day=0, hour=9): commission,
            Resource(classroom, day=2, hour=8): commission,
        }
        penalty = evaluator.evaluate(allocation)
        assert penalty == 0


if __name__ == '__main__':
    unittest.main()