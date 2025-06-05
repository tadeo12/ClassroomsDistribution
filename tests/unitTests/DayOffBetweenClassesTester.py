import unittest
from app.Constraints.Enabled.DayOffBetweenClassesEvaluator import  DayOffBetweenClassesEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *


class TestDayOffBetweenClassesEvaluator(unittest.TestCase):
    def test_2_consecutitives_days_allocation_have_penalty_greater_than_zero(self):
        evaluator = DayOffBetweenClassesEvaluator()
        commission= Commission("commission",Teacher("teacher"), Subject("subject"),10,4)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission,
            Resource(classroom,day=0,hour=1): commission,
            Resource(classroom,day=1,hour=3): commission,
            Resource(classroom,day=1,hour=4): commission,
        }
        penalty= evaluator.evaluate(allocation)        
        assert(penalty>0)

    def test_no_penalty_with_4_hours_classes(self):
        evaluator = DayOffBetweenClassesEvaluator()
        commission= Commission("commission",Teacher("teacher"), Subject("subject"),10,12)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission,
            Resource(classroom,day=0,hour=1): commission,
            Resource(classroom,day=0,hour=2): commission,
            Resource(classroom,day=0,hour=3): commission, 
            Resource(classroom,day=2,hour=0): commission,
            Resource(classroom,day=2,hour=1): commission,
            Resource(classroom,day=2,hour=2): commission,
            Resource(classroom,day=2,hour=3): commission,
            Resource(classroom,day=4,hour=0): commission,
            Resource(classroom,day=4,hour=1): commission,
            Resource(classroom,day=4,hour=2): commission,
            Resource(classroom,day=4,hour=3): commission,
        }
        penalty= evaluator.evaluate(allocation)        
        assert(penalty==0)

    def test_no_penalty_with_2_classes_a_day(self):
        evaluator = DayOffBetweenClassesEvaluator()
        commission= Commission("commission",Teacher("teacher"), Subject("subject"),10,4)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission,
            Resource(classroom,day=0,hour=1): commission,
            Resource(classroom,day=0,hour=2): commission,
            Resource(classroom,day=0,hour=3): commission,
        }
        penalty= evaluator.evaluate(allocation)        
        assert(penalty==0)

    def test_consecutive_classes_on_different_classrooms_has_penalty_greater_than_zero(self):
        evaluator = DayOffBetweenClassesEvaluator()
        commission= Commission("commission",Teacher("teacher"), Subject("subject"),10,4)
        classroom1= Classroom("classroom1",30,Place("place"))
        classroom2= Classroom("classroom2",30,Place("place"))
        allocation = {
            Resource(classroom1,day=0,hour=0): commission,
            Resource(classroom1,day=0,hour=1): commission,
            Resource(classroom2,day=1,hour=3): commission,
            Resource(classroom2,day=1,hour=4): commission,
        }
        penalty= evaluator.evaluate(allocation)        
        assert(penalty>0)

    def test_no_penalty_for_different_commisions_with_classes_on_cosecutive_days(self):
        evaluator = DayOffBetweenClassesEvaluator()
        commission1= Commission("commission1",Teacher("teacher"), Subject("subject"),10,4)
        commission2=Commission("commission2",Teacher("teacher"), Subject("subject"),10,4)
        classroom= Classroom("classroom",30,Place("place"))
        allocation = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=1,hour=3): commission2,
            Resource(classroom,day=1,hour=4): commission2,
        }
        penalty= evaluator.evaluate(allocation)        
        assert(penalty==0)

    def test_more_penalty_with_2_commisions_with_consecutive_days_than_one(self):
        evaluator = DayOffBetweenClassesEvaluator()
        commission1= Commission("commission1",Teacher("teacher"), Subject("subject"),10,4)
        commission2=Commission("commission2",Teacher("teacher"), Subject("subject"),10,4)
        classroom= Classroom("classroom",30,Place("place"))
        allocation1 = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=1,hour=4): commission1,
        }
        allocation2 = {
            Resource(classroom,day=0,hour=0): commission1,
            Resource(classroom,day=0,hour=1): commission1,
            Resource(classroom,day=1,hour=3): commission1,
            Resource(classroom,day=1,hour=4): commission1,
            Resource(classroom,day=2,hour=0): commission2,
            Resource(classroom,day=2,hour=1): commission2,
            Resource(classroom,day=3,hour=3): commission2,
            Resource(classroom,day=3,hour=4): commission2,
        }
        penalty1= evaluator.evaluate(allocation1)
        penalty2= evaluator.evaluate(allocation2)     
        assert(penalty1<penalty2)

if __name__ == '__main__':
    unittest.main()