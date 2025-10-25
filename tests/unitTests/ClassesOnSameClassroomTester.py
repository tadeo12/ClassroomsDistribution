import unittest
from app.Constraints.Enabled.ClassesOnSameClassroomEvaluator import ClassesOnSameClassroomEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *

class TestClassesOnSameClassroomEvaluator(unittest.TestCase):
    def test_no_penalty_with_single_classroom(self):
        evaluator = ClassesOnSameClassroomEvaluator()
        commission = Commission("commission1", Teacher("teacher1"), Subject("subject"), students=10, hoursPerWeek=4)
        classroom = Classroom("classroom1", 30, Place("place"))
        allocation = {
            Resource(classroom, day=0, hour=8): commission,
            Resource(classroom, day=0, hour=9): commission,
            Resource(classroom, day=1, hour=8): commission,
            Resource(classroom, day=1, hour=9): commission,
        }
        penalty = evaluator.evaluate(allocation)
        assert penalty == 0

    def test_penalty_with_two_different_classrooms(self):
        evaluator = ClassesOnSameClassroomEvaluator()
        commission = Commission("commission1", Teacher("teacher1"), Subject("subject"), students=10, hoursPerWeek=4)
        classroom1 = Classroom("classroom1", 30, Place("place"))
        classroom2 = Classroom("classroom2", 30, Place("place"))
        allocation = {
            Resource(classroom1, day=0, hour=8): commission,
            Resource(classroom1, day=0, hour=9): commission,
            Resource(classroom2, day=1, hour=8): commission,
            Resource(classroom2, day=1, hour=9): commission,
        }
        penalty = evaluator.evaluate(allocation)
        assert penalty == 1

    def test_higher_penalty_with_three_classrooms(self):
        evaluator = ClassesOnSameClassroomEvaluator()
        commission = Commission("commission1", Teacher("teacher1"), Subject("subject"), students=10, hoursPerWeek=6)
        classroom1 = Classroom("classroom1", 30, Place("place"))
        classroom2 = Classroom("classroom2", 30, Place("place"))
        classroom3 = Classroom("classroom3", 30, Place("place"))
        allocation = {
            Resource(classroom1, day=0, hour=8): commission,
            Resource(classroom2, day=1, hour=9): commission,
            Resource(classroom3, day=2, hour=10): commission,
        }
        penalty = evaluator.evaluate(allocation)
        assert penalty == 2


if __name__ == '__main__':
    unittest.main()