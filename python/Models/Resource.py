from Classroom import Classroom

class Resource:
    def __init__(self, classroom: Classroom, day: int, hour: int):
        self.classroom = classroom
        self.hour = hour 
        self.day = day

 #   def __str__(self):
  #      return f'Aula {self.aula} - {self.dia}, hora: {self.horario}'