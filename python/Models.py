class Aula:
    def __init__(self, nombre,  capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
    
    def __str__(self):
        return f'Aula {self.nombre} con capacidad para {self.capacidad} alumnos'

class Recurso:
    def __init__(self, aula, dia, horario):
        self.aula = aula  
        self.horario = horario  
        self.dia = dia

    def __str__(self):
        return f'Aula {self.aula} - {self.dia}, hora: {self.horario}'

class Profesor:
    def __init__(self,nombre):
        self.nombre= nombre

    def __str__(self):
        return self.nombre
    
class Materia:
    def __init__(self,nombre):
        self.nombre= nombre

    def __str__(self):
        return self.nombre

class Comision:
    def __init__(self, nombre, profesor, materia, cant_alumnos):
        self.nombre =  nombre
        self.profesor = profesor
        self.materia = materia    
        self.cant_alumnos = cant_alumnos  

    def __str__(self):
        return f'Comisión de {self.materia} - Profesor: {self.profesor}, Cantidad de alumnos: {self.cant_alumnos}'

class Dictado:
    def __init__(self, comision, numero):
        self.comision = comision
        self.numero = numero

    def __str__(self):
        return f'Comisión: {self.comision} - {self.numero}'                                                                                             