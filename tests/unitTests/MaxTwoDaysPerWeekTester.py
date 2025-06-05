import unittest
from unittest.mock import patch

from app.Constraints.Enabled.MaxTwoDaysPerWeekEvaluator import MaxTwoDaysPerWeekEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *

class TestMaxTwoDaysPerWeekEvaluator(unittest.TestCase):

    def test_no_penalty_with_two_classes(self):
        evaluator = MaxTwoDaysPerWeekEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=10)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=0,hour=2): commission1,
            Resource(classroom,day=0,hour=3): commission1,
            Resource(classroom,day=0,hour=4): commission1,
            Resource(classroom,day=1,hour=0): commission1,
            Resource(classroom,day=1,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=1,hour=4): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty==0)

    def test_no_penalty_with_only_a_class(self):
        evaluator = MaxTwoDaysPerWeekEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=10)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=0,hour=2): commission1,
            Resource(classroom,day=0,hour=3): commission1,
            Resource(classroom,day=0,hour=4): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        print(penalty)
        assert(penalty==0)

    def test_three_classes_has_penalty(self):
        evaluator = MaxTwoDaysPerWeekEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=10)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=0,hour=2): commission1,
            Resource(classroom,day=0,hour=3): commission1,
            Resource(classroom,day=1,hour=0): commission1,
            Resource(classroom,day=1,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=3,hour=0): commission1,
            Resource(classroom,day=3,hour=1): commission1,
            Resource(classroom,day=3,hour=2): commission1,
            Resource(classroom,day=3,hour=3): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty>0)

    def test_4_classes_allocation_has_greater_penalty_that_3_class_allocation(self):
        evaluator = MaxTwoDaysPerWeekEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=12)
        classroom= Classroom("classroom",30,Place("place"))
        allocation1 = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=0,hour=2): commission1,
            Resource(classroom,day=0,hour=3): commission1,
            Resource(classroom,day=1,hour=0): commission1,
            Resource(classroom,day=1,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=3,hour=0): commission1,
            Resource(classroom,day=3,hour=1): commission1,
            Resource(classroom,day=3,hour=2): commission1,
            Resource(classroom,day=3,hour=3): commission1,
        }
        allocation2 = {
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=0,hour=2): commission1,
            Resource(classroom,day=0,hour=3): commission1,
            Resource(classroom,day=1,hour=0): commission1,
            Resource(classroom,day=1,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=2,hour=1): commission1,
            Resource(classroom,day=2,hour=2): commission1,
            Resource(classroom,day=2,hour=3): commission1,
            Resource(classroom,day=3,hour=0): commission1,
            Resource(classroom,day=3,hour=1): commission1,
            Resource(classroom,day=3,hour=2): commission1,
        }
        penalty1= evaluator.evaluate(allocation1)
        penalty2= evaluator.evaluate(allocation2)

        assert(penalty2>penalty1)


if __name__ == '__main__':
    unittest.main()    