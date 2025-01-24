from Semester import Semester
from typing import List

class Career:
    def __init__(self, name: str, semesters: List[Semester] = None):
        self.name = name
        self.semesters = semesters if semesters is not None else []