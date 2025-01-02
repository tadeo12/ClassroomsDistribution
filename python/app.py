from Models import *
from RecocidoSimulado import *


# Función principal
def main():
    random.seed()  # Inicializar semilla para números aleatorios

    comisiones = [
    Comision(1, Profesor("Dra. Jesica Carballido"), Materia("Resolución de Problemas y Algoritmos"), 30),
    Comision(2, Profesor("Diego García"), Materia("Resolución de Problemas y Algoritmos"), 30),
    Comision(3, Profesor("Dr. Alejandro García"), Materia("Resolución de Problemas y Algoritmos"), 30),
    Comision(4, Profesor("Dr. Carlos Chesñevar"), Materia("Teoría de la Computabilidad"), 25),
    Comision(5, Profesor("Dr. Sergio Gómez"), Materia("Estructuras de Datos"), 35),
    Comision(6, Profesor("Dr. Martín Larrea"), Materia("Estructuras de Datos"), 35),
    Comision(7, Profesor("Dr. Luciano Tamargo"), Materia("IPOO"), 25),
    Comision(8, Profesor("Dra. Telma Delladio"), Materia("Lenguajes Formales y Autómatas"), 20),
    Comision(9, Profesor("Dra. Andrea Cohen"), Materia("Requerimientos de Sistemas"), 20),
    Comision(10, Profesor("Dra. Laura Cobo"), Materia("Ingeniería de Requisitos"), 25),
    Comision(11, Profesor("Dr. Marcelo Falappa"), Materia("Lógica para Ciencias de la Computación"), 30),
    Comision(12, Profesor("Dr. Sergio Sirmandi"), Materia("Gestión de Calidad en el Software"), 25),
    Comision(13, Profesor("Mg. Karina Cenci"), Materia("Sistemas Distribuidos"), 20),
    Comision(14, Profesor("Dr. Pablo Fillottrani"), Materia("Complejidad y Computabilidad"), 30),
    Comision(15, Profesor("Dr. Sebastián Gottifredi"), Materia("Diseño y Desarrollo de Algoritmos"), 20),
    Comision(16, Profesor("Mg. Mercedes Vitturini"), Materia("Redes de Computadoras"), 25),
    Comision(17, Profesor("Dra. Dana Uribarri"), Materia("Diseño de Interacción y Interfaces para Teleprocesamiento"), 25),
    Comision(18, Profesor("Dra. Dana Uribarri"), Materia("Diseño de Interacción y Interfaces para Teleprocesamiento II"), 20),
    Comision(19, Profesor("Mg. Alejandro Stankevicius"), Materia("Redes de Computadoras"), 20),
    Comision(20, Profesor("Dra. Luján Ganuza"), Materia("Computación Gráfica"), 30),
    Comision(21, Profesor("Dr. Matías Selzer"), Materia("Lenguajes Formales y Autómatas"), 30),
    Comision(22, Profesor("Ing. Leonardo De Matteis"), Materia("Seguridad en Sistemas"), 30),
    Comision(23, Profesor("Ing. Diego Martínez"), Materia("Ingeniería de Aplicaciones Web"), 30),
    Comision(24, Profesor("Dra Elsa Estévez"), Materia("Arquitectura y Diseño de Sistemas"), 30),
    Comision(25, Profesor("Lic. José Moyano"), Materia("Organización y Gestión de Empresas"), 25)
    ]


    # Ejemplo de aulas
    aulas = [
        Aula(1, 25), 
        Aula(2, 30), 
        Aula(3, 40),
        Aula(4, 20),
    ]

    # Parámetros del algoritmo
    iteraciones = 10000
    coef_reduccion_temp = 0.99  # Factor de enfriamiento
    dias = 5  # Días de la semana
    horas = 3  # Horarios por día

    # Ejecutar el algoritmo de Recocido Simulado
    solucion_final = recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas)
    crear_pdf(solucion_final, "opcion1.pdf")
    solucion_final = recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas)
    crear_pdf(solucion_final, "opcion2.pdf")
    solucion_final = recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas)
    crear_pdf(solucion_final, "opcion3.pdf")
    solucion_final = recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas)
    crear_pdf(solucion_final, "opcion4.pdf")
    solucion_final = recocido_simulado(comisiones, aulas, iteraciones, coef_reduccion_temp, dias, horas)
    crear_pdf(solucion_final, "opcion5.pdf")


if __name__ == "__main__":
    main()