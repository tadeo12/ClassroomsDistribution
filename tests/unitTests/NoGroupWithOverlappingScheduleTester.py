import unittest
from app.Constraints.Enabled.NoGroupWithOverlappingScheduleEvaluator import NoGroupWithOverlappingScheduleEvaluator
from app.Models.Resource import *
from app.Models.Commission import *
from app.Models.Teacher import *
from app.Models.Classroom import *
from app.Models.Place import *
from app.Models.Group import *

class TestNoGroupWithOverlappingScheduleEvaluator(unittest.TestCase):

    def setUp(self):
        self.classroom = Classroom("classroom", 30, Place("place"))
        self.teacher = Teacher("teacher1")
        self.subject = Subject("subject")
        self.groupA = Group("A")
        self.groupB = Group("B")

    def test_no_overlap_same_group(self):
        evaluator = NoGroupWithOverlappingScheduleEvaluator()
        commission1 = Commission("c1", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission2 = Commission("c2", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission1.groups = [self.groupA]
        commission2.groups = [self.groupA]
        allocation = {
            Resource(self.classroom, day=0, hour=0): commission1,
            Resource(self.classroom, day=0, hour=1): commission2,  # No overlap
        }
        penalty = evaluator.evaluate(allocation)
        self.assertEqual(penalty, 0)

    def test_overlap_same_group(self):
        evaluator = NoGroupWithOverlappingScheduleEvaluator()
        commission1 = Commission("c1", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission2 = Commission("c2", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission1.groups = [self.groupA]
        commission2.groups = [self.groupA]
        allocation = {
            Resource(self.classroom, day=0, hour=0): commission1,
            Resource(self.classroom, day=0, hour=0): commission2,  # Overlap
        }
        penalty = evaluator.evaluate(allocation)
        self.assertGreater(penalty, 0)

    def test_no_overlap_different_groups(self):
        evaluator = NoGroupWithOverlappingScheduleEvaluator()
        commission1 = Commission("c1", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission2 = Commission("c2", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission1.groups = [self.groupA]
        commission2.groups = [self.groupB]
        allocation = {
            Resource(self.classroom, day=0, hour=0): commission1,
            Resource(self.classroom, day=0, hour=0): commission2,  # Same time, different groups
        }
        penalty = evaluator.evaluate(allocation)
        self.assertEqual(penalty, 0)

    def test_overlap_shared_group(self):
        evaluator = NoGroupWithOverlappingScheduleEvaluator()
        commission1 = Commission("c1", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission2 = Commission("c2", self.teacher, self.subject, students=20, hoursPerWeek=4)
        commission1.groups = [self.groupA, self.groupB]
        commission2.groups = [self.groupB]
        allocation = {
            Resource(self.classroom, day=1, hour=2): commission1,
            Resource(self.classroom, day=1, hour=2): commission2,  # Overlap for groupB
        }
        penalty = evaluator.evaluate(allocation)
        self.assertGreater(penalty, 0)

if __name__ == '__main__':
    unittest.main()