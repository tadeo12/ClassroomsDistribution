import tkinter as tk
from tkinter import ttk

from RecocidoSimulado import recocido_simulado

def obtener_datos():
    # Obtener datos de la interfaz
    num_aulas = int(entry_aulas.get())
    num_horarios = int(entry_horarios.get())
    num_dias = int(entry_dias.get())

    # Crear una lista de comisiones
    comisiones = []
    for i in range(len(lista_comisiones)):
        comision = {
            'profesor': lista_comisiones[i].get('profesor'),
            'materia': lista_comisiones[i].get('materia'),
            'alumnos': int(lista_comisiones[i].get('alumnos'))
        }
        comisiones.append(comision)

    # Valores por defecto para iteraciones y coeficiente de reducción de temperatura
    iteraciones = 1000
    coef_reduccion_temp = 0.95

    # Llamar a la función de recocido simulado
    recocido_simulado(comisiones, num_aulas, iteraciones, coef_reduccion_temp, num_dias, num_horarios)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Asignación de Aulas")

# Crear etiquetas y campos de entrada
label_aulas = tk.Label(ventana, text="Número de aulas:")
entry_aulas = tk.Entry(ventana)
label_horarios = tk.Label(ventana, text="Número de horarios por día:")
entry_horarios = tk.Entry(ventana, textvariable=tk.StringVar(value=3))
label_dias = tk.Label(ventana, text="Número de días:")
entry_dias = tk.Entry(ventana, textvariable=tk.StringVar(value=5))

# Crear una lista para almacenar las comisiones
lista_comisiones = []

# Función para agregar una nueva comisión
def agregar_comision():
    nueva_comision = {
        'profesor': tk.StringVar(),
        'materia': tk.StringVar(),
        'alumnos': tk.StringVar()
    }
    lista_comisiones.append(nueva_comision)

    # Crear etiquetas y campos de entrada para la nueva comisión
    label_profesor = tk.Label(ventana, text="Profesor:")
    entry_profesor = tk.Entry(ventana, textvariable=nueva_comision['profesor'])
    label_materia = tk.Label(ventana, text="Materia:")
    entry_materia = tk.Entry(ventana, textvariable=nueva_comision['materia'])
    label_alumnos = tk.Label(ventana, text="Número de alumnos:")
    entry_alumnos = tk.Entry(ventana, textvariable=nueva_comision['alumnos'])

    # Agregar los elementos a la ventana
    ventana.grid_rowconfigure(len(lista_comisiones) * 3 - 1, minsize=20)
    label_profesor.grid(row=len(lista_comisiones) * 3, column=0, sticky="e")
    entry_profesor.grid(row=len(lista_comisiones) * 3, column=1)
    label_materia.grid(row=len(lista_comisiones) * 3 + 1, column=0, sticky="e")
    entry_materia.grid(row=len(lista_comisiones) * 3 + 1, column=1)
    label_alumnos.grid(row=len(lista_comisiones) * 3 + 2, column=0, sticky="e")
    entry_alumnos.grid(row=len(lista_comisiones) * 3 + 2, column=1)

# Botón para agregar una nueva comisión
boton_agregar = tk.Button(ventana, text="Agregar Comisión", command=agregar_comision)

# Botón para ejecutar el algoritmo
boton_ejecutar = tk.Button(ventana, text="Ejecutar", command=obtener_datos)

# Agregar los elementos a la ventana
label_aulas.grid(row=0, column=0, sticky="e")
entry_aulas.grid(row=0, column=1)
label_horarios.grid(row=1, column=0, sticky="e")
entry_horarios.grid(row=1, column=1)
label_dias.grid(row=2, column=0, sticky="e")
entry_dias.grid(row=2, column=1)
boton_agregar.grid(row=3, column=0, columnspan=2)
boton_ejecutar.grid(row=4, column=0, columnspan=2)

ventana.mainloop()