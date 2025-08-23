from .Place import Place
from ConfigManager import ConfigManager  # Asegúrate de que este import sea válido


class Classroom:
    def __init__(self, name: str, capacity: int, place: Place):
        self.name = name
        self.capacity = capacity
        self.place = place  # edificio o sede

    def __str__(self):
        return f'Aula {self.name} con capacidad para {self.capacity} alumnos, ubicada en {self.place}'
