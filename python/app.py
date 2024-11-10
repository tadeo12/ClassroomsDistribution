from Models import *
from RecocidoSimulado import *


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
    iteraciones = 1000
    coef_reduccion_temp = 0.99  # Factor de enfriamiento
    dias = 5  # Días de la semana
    horas = 2  # Horarios por día

    # Ejecutar el algoritmo de Recocido Simulado
    solucion_final = recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas)
    
    
    print(solucion_final)

    #df=pd.DataFrame(solucion_final)
    #print(df)

#    # Imprimir la solución final
#    for i, (dictado, recurso) in enumerate(solucion_final.items()):
#        print(f"comision {dictado.comision.nombre} (alumnos: {dictado.comision.cant_alumnos}) "
#              f"asignada a aula {recurso.aula} (capacidad: {recurso.aula.capacidad}), "
#              f"día {recurso.dia}, hora {recurso.horario}")
#
#    resultado_evaluacion = evaluar(solucion_final)
#    print(f"Resultado de la evaluación: {resultado_evaluacion}")

if __name__ == "__main__":
    main()