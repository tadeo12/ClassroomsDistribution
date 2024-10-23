import random
import math
from Models import *

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

def evaluar(distribucion):
    #TODO separarlo de la logica del algoritmo
    penalizacion = 0

    # Penalización por capacidad del aula
    for dictado, recurso in distribucion.items():
        if dictado.comision.cant_alumnos > recurso.aula.capacidad:
            penalizacion += 100  # Penalización por exceso de alumnos

    # Penalización por asignar c1 y c2 al mismo día
    dictados = list(distribucion.items())  # Convertimos el map a una lista
    for i in range(len(dictados)):
        dictado1, recurso1 = dictados[i]
        for j in range(i + 1, len(dictados)):
            dictado2, recurso2 = dictados[j]

            # Si es la misma comisión y ambos dictados están en el mismo día
            if dictado1.comision == dictado2.comision and recurso1.dia == recurso2.dia:
                penalizacion += 1  # Penalización por ambos dictados el mismo día

    return penalizacion

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


# Función principal
def main():
    random.seed()  # Inicializar semilla para números aleatorios

    comisiones = [
        Comision(1,Profesor("Prof. Gomez"), Materia("Matematicas"), 30),
        Comision(2,Profesor("Prof. Perez"), Materia("Fisica"), 25),
        Comision(3,Profesor("Prof. Lopez"), Materia("Quimica"), 40),
        Comision(4,Profesor("Prof. Gomez"), Materia("Matematicas2"), 30),
        Comision(5,Profesor("Prof. Perez"), Materia("Fisica2"), 25),
        Comision(6,Profesor("Prof. Lopez"), Materia("Quimica2"), 40),
        Comision(7,Profesor("Prof. Gomez"), Materia("Matematicas3"), 30),
        Comision(8,Profesor("Prof. Perez"), Materia("Fisica3"), 25),
        Comision(9,Profesor("Prof. Lopez"), Materia("Quimica3"), 40)
    ]

    # Ejemplo de aulas
    aulas = [
        Aula(1, 25), 
        Aula(2, 30), 
        Aula(3, 40)
    ]

    # Parámetros del algoritmo
    iteraciones = 10
    coef_reduccion_temp = 0.99  # Factor de enfriamiento
    dias = 5  # Días de la semana
    horas = 2  # Horarios por día

    # Ejecutar el algoritmo de Recocido Simulado
    solucion_final = recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas)

    # Imprimir la solución final
    for i, (dictado, recurso) in enumerate(solucion_final.items()):
        print(f"comision {dictado.comision.nombre} (alumnos: {dictado.comision.cant_alumnos}) "
              f"asignada a aula {recurso.aula} (capacidad: {recurso.aula.capacidad}), "
              f"día {recurso.dia}, hora {recurso.horario}")

    resultado_evaluacion = evaluar(solucion_final)
    print(f"Resultado de la evaluación: {resultado_evaluacion}")

if __name__ == "__main__":
    main()