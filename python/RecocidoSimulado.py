import random
import math
from Models import *
from GenerarPDF import *
from Evaluar import evaluar

def generar_dictados(comisiones):
    dictados = []
    for comision in comisiones:
        dictados.append(Dictado(comision, 1))
        dictados.append(Dictado(comision, 2))  
    return dictados

def generar_recursos(aulas, dias, horarios):
    recursos = []
    for aula in aulas:
        for dia in range(dias):
            for horario in range(horarios):
                recursos.append(Recurso(aula, dia, horario))
    return recursos

def generar_distribucion_inicial(dictados, recursos, recursos_disponibles):
    distribucion = {}
    random.shuffle(recursos)
    
    # Asignar dictados a recursos
    for i in range(len(dictados)):
        distribucion[dictados[i]] = recursos[i]
        recursos_disponibles.remove(recursos[i]) 
    
    return distribucion

def generar_vecino(distribucion, recursos_disponibles):

    vecino = distribucion.copy()
    dictado = random.choice(list(vecino.keys()))
    recurso_actual = vecino[dictado]
    nuevo_recurso = random.choice(list(recursos_disponibles))
    recursos_disponibles.remove(nuevo_recurso)
    recursos_disponibles.add(recurso_actual)
    vecino[dictado] = nuevo_recurso

    return vecino


def recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas):
    dictados = generar_dictados(comisiones)
    recursos = generar_recursos(aulas, dias, horas)

    recursos_disponibles = set(recursos)

    solucion = generar_distribucion_inicial(dictados, recursos, recursos_disponibles)
    costo_solucion = evaluar(solucion)

    actual = solucion
    costo_actual = costo_solucion
    temperatura = 1.0

    for i in range(iteraciones):
        recursos_disponibles_copia = recursos_disponibles.copy()  # copia en profundidad
        vecino = generar_vecino(actual, recursos_disponibles_copia)  # actualiza los recursos disponibles en la copia
        costo_vecino = evaluar(vecino)

        diferencia = costo_vecino - costo_actual

        if diferencia < 0:
            actual = vecino
            costo_actual = costo_vecino
            solucion = vecino
            costo_solucion = costo_vecino
            recursos_disponibles = recursos_disponibles_copia
        else:
            if math.exp(-diferencia / temperatura) > random.random():
                actual = vecino
                costo_actual = costo_vecino
                recursos_disponibles = recursos_disponibles_copia

        temperatura *= coef_reduccion_temp

    return solucion

