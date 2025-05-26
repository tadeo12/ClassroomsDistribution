from .Teacher import Teacher
from .Subject import Subject


class Commission:
    def __init__(self, name: str, teacher: Teacher, subject: Subject, students: int, hoursPerWeek: int = 8):      
        self.name =  name
        self.teacher = teacher
        self.subject = subject    
        self.students = students
        self.hours = hoursPerWeek
        self.groups = []

    
    def __str__(self):
        return f'Comisión de {self.subject} - Profesor: {self.teacher}, Cantidad de alumnos: {self.students}, Horas por semana: {self.hours}'