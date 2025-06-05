import unittest
from app.Constraints.Enabled.NoOverlappingTeachersScheduleEvaluator import NoOverlappingTeachersScheduleEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *
from app.Models.Subject import *

class TestNoOverlappingTeachersScheduleEvaluator(unittest.TestCase):

    def setUp(self):
        self.classroom1 = Classroom("classroom1", 30, Place("place"))
        self.classroom2 = Classroom("classroom2", 30, Place("place"))
        self.teacher = Teacher("teacher1")
        self.subject1 = Subject("subject1")
        self.subject2 = Subject("subject2")

    def test_no_overlap(self):
        evaluator = NoOverlappingTeachersScheduleEvaluator()
        commission1 = Commission("c1", self.teacher, self.subject1, students=20, hoursPerWeek=4)
        commission2 = Commission("c2", self.teacher, self.subject2, students=20, hoursPerWeek=4)
        allocation = {
            Resource(self.classroom1, day=0, hour=0): commission1,
            Resource(self.classroom2, day=0, hour=1): commission2,  # Different hour, no overlap
        }
        penalty = evaluator.evaluate(allocation)
        self.assertEqual(penalty, 0)

    def test_overlap_same_teacher(self):
        evaluator = NoOverlappingTeachersScheduleEvaluator()
        commission1 = Commission("c1", self.teacher, self.subject1, students=20, hoursPerWeek=4)
        commission2 = Commission("c2", self.teacher, self.subject2, students=20, hoursPerWeek=4)
        allocation = {
            Resource(self.classroom1, day=0, hour=0): commission1,
            Resource(self.classroom2, day=0, hour=0): commission2,  # Same hour, different classroom
        }
        penalty = evaluator.evaluate(allocation)
        self.assertGreater(penalty, 0)

    def test_no_penalty_same_classroom(self):
        evaluator = NoOverlappingTeachersScheduleEvaluator()
        commission1 = Commission("c1", self.teacher, self.subject1, students=20, hoursPerWeek=4)
        commission2 = Commission("c2", self.teacher, self.subject2, students=20, hoursPerWeek=4)
        allocation = {
            Resource(self.classroom1, day=0, hour=0): commission1,
            Resource(self.classroom1, day=0, hour=0): commission2,  # Same classroom, should not penalize
        }
        penalty = evaluator.evaluate(allocation)
        self.assertEqual(penalty, 0)

if __name__ == '__main__':
    unittest.main()