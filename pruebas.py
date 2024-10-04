import random
import math

# Función que evalúa cuántas restricciones se incumplen en una solución
def evaluar_restricciones(solucion, aulas, capacidad_aulas):
    # Aquí evaluarás cuántas restricciones incumple la solución:
    # 1. Capacidad de las aulas
    # 2. Clases que duran más de lo permitido
    # 3. Conflictos de horario
    restricciones_incumplidas = 0
    
    # Ejemplo de evaluación de una restricción de capacidad de aulas
    for clase, aula in solucion.items():
        if capacidad_aulas[aula] < clase['num_estudiantes']:
            restricciones_incumplidas += 1  # Incumple la capacidad del aula
    
    # Otras evaluaciones pueden añadirse aquí
    return restricciones_incumplidas

# Genera una solución vecina realizando un cambio en la asignación de aulas o franjas horarias
def generar_vecino(solucion_actual, aulas, franjas_horarias):
    nueva_solucion = solucion_actual.copy()
    
    # Realizar un cambio aleatorio: cambiar una clase de aula o franja horaria
    clase_a_cambiar = random.choice(list(nueva_solucion.keys()))
    if random.choice([True, False]):
        # Cambiar aula
        nueva_solucion[clase_a_cambiar]['aula'] = random.choice(aulas)
    else:
        # Cambiar franja horaria
        nueva_solucion[clase_a_cambiar]['franja_horaria'] = random.choice(franjas_horarias)
    
    return nueva_solucion

def inicializarDistribucion(aulas,capacidad_aulas, franjas_horarias, comisiones):


    return {comision: {'aula': random.choice(aulas), 'franja_horaria': random.choice(franjas_horarias)} for comision in comisiones}

# Implementación del algoritmo de recocido simulado
def recocido_simulado(aulas, capacidad_aulas, franjas_horarias, comisiones, temperatura_inicial, tasa_enfriamiento, iteraciones):
    # Inicialización
    solucion_actual = inicializarDistribucion(aulas, capacidad_aulas, franjas_horarias, comisiones) 
    mejor_solucion = solucion_actual
    temperatura = temperatura_inicial
    
    # Ciclo principal del algoritmo
    for i in range(iteraciones):
        # Genera una nueva solución vecina
        nueva_solucion = generar_vecino(solucion_actual, aulas, franjas_horarias)
        
        # Calcula el cambio en la cantidad de restricciones incumplidas
        delta = evaluar_restricciones(nueva_solucion, aulas, capacidad_aulas) - evaluar_restricciones(solucion_actual, aulas, capacidad_aulas)
        
        # Si la nueva solución es mejor, la aceptamos
        if delta < 0:
            solucion_actual = nueva_solucion
        else:
            # Si es peor, la aceptamos con una probabilidad que depende de la temperatura
            probabilidad_aceptacion = math.exp(-delta / temperatura)
            if random.uniform(0, 1) < probabilidad_aceptacion:
                solucion_actual = nueva_solucion
        
        # Actualizamos la mejor solución encontrada
        if evaluar_restricciones(solucion_actual, aulas, capacidad_aulas) < evaluar_restricciones(mejor_solucion, aulas, capacidad_aulas):
            mejor_solucion = solucion_actual
        
        # Enfriamos el sistema (reducimos la temperatura)
        temperatura *= tasa_enfriamiento
    return mejor_solucion

# Parámetros del problema
aulas = ['Aula 1', 'Aula 2', 'Aula 3']
capacidad_aulas = {'Aula 1': 30, 'Aula 2': 40, 'Aula 3': 50}
franjas_horarias = ['8-10', '10-12', '12-14', '14-16', '16-18', '18-20']
dias = ['Lunes', 'Martes','Miercoles','Jueves','Viernes']

recursos = []
for d in dias:
    for a in aulas:
        for h in franjas_horarias:
            recursos.append({'dia': d, 'aula': a, 'hora': h})


print(recursos, sep= "/n")
print(len(recursos))


comisiones = [{'nombre': 'Matemáticas', 'num_estudiantes': 35}, {'nombre': 'Física', 'num_estudiantes': 25}, {'nombre': 'Química', 'num_estudiantes': 45}]

# Ejecutar el recocido simulado
#mejor_solucion = recocido_simulado(aulas, capacidad_aulas, franjas_horarias, comisiones, temperatura_inicial=1000, tasa_enfriamiento=0.95, iteraciones=1000)
#print("Mejor solución encontrada:", mejor_solucion)
