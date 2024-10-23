import tkinter as tk
from tkinter import ttk
from itertools import product

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Recursos y Comisiones")

        # Variables para almacenar franjas horarias, días y aulas
        self.franjas_horarias = []
        self.dias = []
        self.aulas = []

        # Sección de franjas horarias
        self.label_franjas = ttk.Label(root, text="Franjas Horarias (ej. 8:00-10:00)")
        self.label_franjas.grid(row=0, column=0, padx=10, pady=10)

        # Definimos columnas en el Treeview, y el identificador de columna debe ser simple
        self.tree_franjas = ttk.Treeview(root, columns=("franja"), show="headings")
        self.tree_franjas.heading("franja", text="Franja Horaria")  # Cambiamos "Franja Horaria" a "franja"
        self.tree_franjas.grid(row=1, column=0, padx=10, pady=10)

        self.frame_franjas = ttk.Frame(root)
        self.frame_franjas.grid(row=2, column=0, padx=10, pady=10)

        self.label_franja = ttk.Label(self.frame_franjas, text="Franja Horaria:")
        self.label_franja.grid(row=0, column=0)
        self.entry_franja = ttk.Entry(self.frame_franjas)
        self.entry_franja.grid(row=0, column=1)

        self.boton_agregar_franja = ttk.Button(self.frame_franjas, text="Agregar Franja", command=self.agregar_franja)
        self.boton_agregar_franja.grid(row=1, columnspan=2)

        # Sección de días
        self.label_dias = ttk.Label(root, text="Días (ej. Lunes, Martes)")
        self.label_dias.grid(row=0, column=1, padx=10, pady=10)

        self.tree_dias = ttk.Treeview(root, columns=("dia"), show="headings")
        self.tree_dias.heading("dia", text="Día")  # Definimos columna con el identificador "dia"
        self.tree_dias.grid(row=1, column=1, padx=10, pady=10)

        self.frame_dias = ttk.Frame(root)
        self.frame_dias.grid(row=2, column=1, padx=10, pady=10)

        self.label_dia = ttk.Label(self.frame_dias, text="Día:")
        self.label_dia.grid(row=0, column=0)
        self.entry_dia = ttk.Entry(self.frame_dias)
        self.entry_dia.grid(row=0, column=1)

        self.boton_agregar_dia = ttk.Button(self.frame_dias, text="Agregar Día", command=self.agregar_dia)
        self.boton_agregar_dia.grid(row=1, columnspan=2)

        # Sección de aulas
        self.label_aulas = ttk.Label(root, text="Aulas")
        self.label_aulas.grid(row=0, column=2, padx=10, pady=10)

        self.tree_aulas = ttk.Treeview(root, columns=("aula"), show="headings")
        self.tree_aulas.heading("aula", text="Aula")  # Definimos columna con el identificador "aula"
        self.tree_aulas.grid(row=1, column=2, padx=10, pady=10)

        self.frame_aulas = ttk.Frame(root)
        self.frame_aulas.grid(row=2, column=2, padx=10, pady=10)

        self.label_aula = ttk.Label(self.frame_aulas, text="Aula:")
        self.label_aula.grid(row=0, column=0)
        self.entry_aula = ttk.Entry(self.frame_aulas)
        self.entry_aula.grid(row=0, column=1)

        self.boton_agregar_aula = ttk.Button(self.frame_aulas, text="Agregar Aula", command=self.agregar_aula)
        self.boton_agregar_aula.grid(row=1, columnspan=2)

        # Botón para generar recursos
        self.boton_generar_recursos = ttk.Button(root, text="Generar Recursos", command=self.generar_recursos)
        self.boton_generar_recursos.grid(row=3, column=1, padx=10, pady=10)

        # Sección de recursos generados
        self.label_recursos = ttk.Label(root, text="Recursos Generados (Aula, Día, Franja Horaria)")
        self.label_recursos.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.tree_recursos = ttk.Treeview(root, columns=("aula", "dia", "franja"), show="headings")
        self.tree_recursos.heading("aula", text="Aula")
        self.tree_recursos.heading("dia", text="Día")
        self.tree_recursos.heading("franja", text="Franja Horaria")  # Columna con identificador "franja"
        self.tree_recursos.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def agregar_franja(self):
        franja = self.entry_franja.get()
        if franja:
            self.franjas_horarias.append(franja)
            self.tree_franjas.insert("", "end", values=(franja,))
            self.entry_franja.delete(0, tk.END)

    def agregar_dia(self):
        dia = self.entry_dia.get()
        if dia:
            self.dias.append(dia)
            self.tree_dias.insert("", "end", values=(dia,))
            self.entry_dia.delete(0, tk.END)

    def agregar_aula(self):
        aula = self.entry_aula.get()
        if aula:
            self.aulas.append(aula)
            self.tree_aulas.insert("", "end", values=(aula,))
            self.entry_aula.delete(0, tk.END)

    def generar_recursos(self):
        # Borrar recursos previos
        for item in self.tree_recursos.get_children():
            self.tree_recursos.delete(item)

        # Generar combinaciones de recursos
        recursos = product(self.aulas, self.dias, self.franjas_horarias)
        for aula, dia, franja in recursos:
            self.tree_recursos.insert("", "end", values=(aula, dia, franja))


# Crear la ventana principal de la aplicación
root = tk.Tk()
app = Aplicacion(root)
root.mainloop()
