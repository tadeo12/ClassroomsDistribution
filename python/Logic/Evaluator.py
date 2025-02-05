import logging
from .ConstraintLoader import load_evaluation_functions


def evaluate(allocation: dict):
    functions = load_evaluation_functions()
    totalCost=0
    info = ""
    for function, evaluatorClass in functions.items():
        cost=  evaluatorClass().evaluate(allocation)
        info += f"penalizacion de '{function}' : {cost}\n"
        print(info)
        if cost is not None:
            totalCost +=  cost
        else:
            logging.error(f"Error al calcular la penalizacion de {function}")
    return totalCost, info


#def evaluar(distribucion):
    #penalizacion = 0
    ## Penalización por capacidad del aula
    #for dictado, recurso in distribucion.items():
        #if dictado.comision.cant_alumnos > recurso.aula.capacidad:
            #penalizacion += 100  # Penalización por exceso de alumnos

    ## Penalización por asignar c1 y c2 al mismo día
    #dictados = list(distribucion.items())  # Convertimos el map a una lista
    #for i in range(len(dictados)):
        #dictado1, recurso1 = dictasdos[i]
        #for j in range(i + 1, len(dictados)):
            #dictado2, recurso2 = dictados[j]

            ## Si es la misma comisión y ambos dictados están en el mismo día
            #if dictado1.comision == dictado2.comision and recurso1.dia == recurso2.dia:
                #penalizacion += 1  # Penalización por ambos dictados el mismo día
    #return penalizacion
