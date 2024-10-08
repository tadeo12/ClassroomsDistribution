
from Models import *

PENALIZACION_CAPACIDAD = 50

class Distibución:
    def __init__(self, asignacion, restricciones):
        self.asignacion = asignacion #mapeo dictado -> recurso
        self.puntaje = self.evaluar() 

    def evaluar(self):
        f = 0
        for dictado in self.asignacion:
            if (dictado.comision.cant_alumnos > asignacion[dictado].aula.capacidad)
                f += PENALIZACION_CAPACIDAD
                
        return f

