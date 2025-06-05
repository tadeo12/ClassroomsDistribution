import unittest
from unittest.mock import patch

from app.Constraints.Enabled.MaxOneClassPerDayEvaluator import MaxOneClassPerDayEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *

class TestMaxOneClassPerDayEvaluator(unittest.TestCase):

    def test_no_penalty_with_classes_of_5_hours(self):
        evaluator = MaxOneClassPerDayEvaluator()
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

    def test_two_classes_on_same_day_has_penalty(self):
        evaluator = MaxOneClassPerDayEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=1,hour=0): commission1,
            Resource(classroom,day=1,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=1,hour=7): commission1,
            Resource(classroom,day=1,hour=8): commission1,
            Resource(classroom,day=1,hour=9): commission1,
            Resource(classroom,day=1,hour=10): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty>0)


    def test_no_penalty_with_diferents_commisions_on_same_day(self):
        evaluator = MaxOneClassPerDayEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
        commission2 = Commission("commission2", Teacher("teacher2"), Subject("subject"),students=20,hoursPerWeek=8)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=1,hour=0): commission1,
            Resource(classroom,day=1,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=1,hour=7): commission2,
            Resource(classroom,day=1,hour=8): commission2,
            Resource(classroom,day=1,hour=9): commission2,
            Resource(classroom,day=1,hour=10): commission2,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty==0)
    
if __name__ == '__main__':
    unittest.main()    