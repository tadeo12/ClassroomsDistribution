import unittest
from app.Constraints.Enabled.EnoughCapacityEvaluator import EnoughCapacityEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *

class TestEnoughCapacityEvaluator(unittest.TestCase):
    def test_no_penalty_with_less_students_that_capacity(self):
        evaluator = EnoughCapacityEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
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
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty==0)


    def test_no_penalty_with_same_capacity_that_students(self):
        evaluator = EnoughCapacityEvaluator()
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

    def test_penalty_greater_that_zero_with_less_capacity_some_days(self):
        evaluator = EnoughCapacityEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=12)
        classroom1= Classroom("classroom1",20,Place("place"))
        classroom2= Classroom("classroom2",10,Place("place"))
        allocation = {
            Resource(classroom1,day=0,hour=0): commission1,
            Resource(classroom1,day=0,hour=1): commission1,
            Resource(classroom1,day=0,hour=2): commission1,
            Resource(classroom1,day=0,hour=3): commission1,
            Resource(classroom2,day=1,hour=0): commission1,
            Resource(classroom2,day=1,hour=1): commission1,
            Resource(classroom2,day=1,hour=2): commission1,
            Resource(classroom2,day=1,hour=3): commission1,
            Resource(classroom1,day=2,hour=0): commission1,
            Resource(classroom1,day=2,hour=1): commission1,
            Resource(classroom1,day=2,hour=2): commission1,
            Resource(classroom1,day=2,hour=3): commission1,
        }
        penalty= evaluator.evaluate(allocation)
        assert(penalty>0)

    def test_greater_penalty_with_more_assignments_of_classrooms_with_insufficient_capacity(self):
        evaluator = EnoughCapacityEvaluator()
        commission1 = Commission("commission1", Teacher("teacher1"), Subject("subject"),students=20,hoursPerWeek=8)
        bigClassroom= Classroom("classroom1",20,Place("place"))
        smallClassroom= Classroom("classroom2",10,Place("place"))
        allocation1 = {
            Resource(bigClassroom,day=0,hour=0): commission1,
            Resource(bigClassroom,day=0,hour=1): commission1,
            Resource(bigClassroom,day=0,hour=2): commission1,
            Resource(bigClassroom,day=0,hour=3): commission1,
            Resource(smallClassroom,day=1,hour=0): commission1,
            Resource(smallClassroom,day=1,hour=1): commission1,
            Resource(smallClassroom,day=1,hour=2): commission1,
            Resource(smallClassroom,day=1,hour=3): commission1,
        }
        allocation2 = {
            Resource(smallClassroom,day=0,hour=0): commission1,
            Resource(smallClassroom,day=0,hour=1): commission1,
            Resource(smallClassroom,day=0,hour=2): commission1,
            Resource(smallClassroom,day=0,hour=3): commission1,
            Resource(smallClassroom,day=1,hour=0): commission1,
            Resource(smallClassroom,day=1,hour=1): commission1,
            Resource(smallClassroom,day=1,hour=2): commission1,
            Resource(smallClassroom,day=1,hour=3): commission1,
        }
        penalty1= evaluator.evaluate(allocation1)
        penalty2= evaluator.evaluate(allocation2)
        assert(penalty2>penalty1)
    
if __name__ == '__main__':
    unittest.main()    