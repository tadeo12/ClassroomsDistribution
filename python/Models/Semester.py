from typing import List
from .Subject import Subject
#from Career import Career

class Semester:

    def __init__(self, semester_name: str,subjects: List[Subject] = None):
        #self.carrer = career
        self.semester_name = semester_name
        self.subjects = subjects if subjects is not None else []

    def add_subject(self, subject: Subject):
        self.subjects.append(subject)