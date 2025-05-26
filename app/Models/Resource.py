from .Classroom import Classroom

class Resource:
    _counter = 0

    def __init__(self, classroom: Classroom, day: int, hour: int):
        self.id = Resource._counter
        Resource._counter += 1
        self.classroom = classroom
        self.hour = hour 
        self.day = day

    def __str__(self):
        return f'Aula {self.classroom.name} - {self.day}, hora: {self.hour}'