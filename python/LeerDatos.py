import json
from Models import *

ruta_json = "./datos.json"

def cargar_datos():
    with open(ruta_json, 'r') as archivo:
        datos = json.load(archivo)
    
    # Cargar comisiones
    comisiones = [
        Comision(c["id"], c["profesor"], c["materia"], c["alumnos"]) 
        for c in datos["comisiones"]
    ]
    
    # Cargar aulas
    aulas = [Aula(a["id"], a["capacidad"]) for a in datos["aulas"]]
    
    # Cargar parámetros generales
    parametros = datos["parametros"]
    
    return comisiones, aulas, parametros