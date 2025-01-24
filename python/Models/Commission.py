from Teacher import Teacher
from Subject import Subject
from Career import Career 
from typing import List



class Commission:
    def __init__(self, name: str, teacher: Teacher, subject: Subject, students: int, careers: List[Career] = None):
        self.name =  name
        self.teacher = teacher
        self.subject = subject    
        self.students = students
        self.careers = careers if careers is not None else []
    
    #def add_career(self, career: Career):
        #if career not in self.careers:  # Evitar duplicados
            #self.careers.append(career)

    #def get_careers(self):
        #return self.careers
    
   # def __str__(self):
   #    return f'Comisión de {self.materia} - Profesor: {self.profesor}, Cantidad de alumnos: {self.cant_alumnos}'