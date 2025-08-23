import unittest
from unittest.mock import patch

from app.Constraints.Enabled.Max4HoursPerClassEvaluator import Max4HoursPerClassEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *

class TestMax4HoursPerClassesEvaluator(unittest.TestCase):

    @patch('app.Constraints.Enabled.Max4HoursPerClassesEvaluator.HOURS_PER_RESOURCE', new=1)
    def test_no_penalty_with_less_hours_per_class(self):
        evaluator = Max4HoursPerClassEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=0,hour=2): commission1,
            Resource(classroom,day=1,hour=0): commission1,
            Resource(classroom,day=1,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=2,hour=5): commission1,
            Resource(classroom,day=2,hour=6): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty==0)

    @patch('app.Constraints.Enabled.Max4HoursPerClassesEvaluator.HOURS_PER_RESOURCE', new=1)
    def test_no_penalty_4_hours_per_class(self):
        evaluator = Max4HoursPerClassEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
        classroom= Classroom("classroom",20,Place("place"))
        allocation = {
            Resource(classroom,day=2,hour=0): commission1,
            Resource(classroom,day=2,hour=1): commission1,
            Resource(classroom,day=2,hour=2): commission1,
            Resource(classroom,day=2,hour=3): commission1,
            Resource(classroom,day=3,hour=0): commission1,
            Resource(classroom,day=3,hour=1): commission1,
            Resource(classroom,day=3,hour=2): commission1,
            Resource(classroom,day=3,hour=3): commission1
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty==0)

    @patch('app.Constraints.Enabled.Max4HoursPerClassesEvaluator.HOURS_PER_RESOURCE', new=2)
    def test_no_penalty_4_hours_per_class_with_less_resources(self):
        evaluator = Max4HoursPerClassEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
        classroom= Classroom("classroom",20,Place("place"))
        allocation = {
            Resource(classroom,day=2,hour=0): commission1,
            Resource(classroom,day=2,hour=1): commission1,
            Resource(classroom,day=3,hour=2): commission1,
            Resource(classroom,day=3,hour=3): commission1
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty==0)

    @patch('app.Constraints.Enabled.Max4HoursPerClassesEvaluator.HOURS_PER_RESOURCE', new=0.5)
    def test_no_penalty_4_hours_per_class_with_more_resources(self):
        evaluator = Max4HoursPerClassEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=12)
        classroom1= Classroom("classroom1",20,Place("place"))
        classroom2= Classroom("classroom2",10,Place("place"))
        allocation = {
            Resource(classroom1,day=0,hour=0): commission1,
            Resource(classroom1,day=0,hour=1): commission1,
            Resource(classroom1,day=0,hour=2): commission1,
            Resource(classroom1,day=0,hour=3): commission1,
            Resource(classroom1,day=0,hour=4): commission1,
            Resource(classroom1,day=0,hour=5): commission1,
            Resource(classroom1,day=0,hour=6): commission1,
            Resource(classroom1,day=0,hour=7): commission1,
            Resource(classroom2,day=1,hour=0): commission1,
            Resource(classroom2,day=1,hour=1): commission1,
            Resource(classroom2,day=1,hour=2): commission1,
            Resource(classroom2,day=1,hour=3): commission1,
            Resource(classroom2,day=1,hour=4): commission1,
            Resource(classroom2,day=1,hour=5): commission1,
            Resource(classroom2,day=1,hour=6): commission1,
            Resource(classroom2,day=1,hour=7): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty==0)

    @patch('app.Constraints.Enabled.Max4HoursPerClassesEvaluator.HOURS_PER_RESOURCE', new=1)
    def test_5_hours_classes_has_penalty(self):
        evaluator = Max4HoursPerClassEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
        classroom= Classroom("classroom",20,Place("place"))
        allocation = {
            Resource(classroom,day=2,hour=0): commission1,
            Resource(classroom,day=2,hour=1): commission1,
            Resource(classroom,day=2,hour=2): commission1,
            Resource(classroom,day=2,hour=3): commission1,
            Resource(classroom,day=2,hour=4): commission1,
            Resource(classroom,day=3,hour=0): commission1,
            Resource(classroom,day=3,hour=1): commission1,
            Resource(classroom,day=3,hour=2): commission1,
            Resource(classroom,day=3,hour=3): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty>0)    


    @patch('app.Constraints.Enabled.Max4HoursPerClassesEvaluator.HOURS_PER_RESOURCE', new=1)
    def test_has_more_penalty_2_commisions_with_5_hour_classes_that_only_one(self):
        evaluator = Max4HoursPerClassEvaluator()
        commission1= Commission("commission1",Teacher("teacher"), Subject("subject"),10,4)
        commission2=Commission("commission2",Teacher("teacher"), Subject("subject"),10,4)
        classroom= Classroom("classroom",30,Place("place"))
        allocation1 = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=0,hour=3): commission1,
            Resource(classroom,day=0,hour=4): commission1,
            Resource(classroom,day=0,hour=5): commission1,
        }
        allocation2 = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=1,hour=2): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=2,hour=0): commission2,
            Resource(classroom,day=2,hour=1): commission2,
            Resource(classroom,day=2,hour=2): commission2,
            Resource(classroom,day=2,hour=3): commission2,
            Resource(classroom,day=2,hour=4): commission2,
        }
        penalty1= evaluator.evaluate(allocation1)
        penalty2= evaluator.evaluate(allocation2)     
        assert(penalty1<penalty2)   
    
if __name__ == '__main__':
    unittest.main()    