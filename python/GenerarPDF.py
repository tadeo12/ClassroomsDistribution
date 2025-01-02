from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from Evaluar import evaluar


styles = getSampleStyleSheet()

# Función para llenar la matriz de datos
def cargarDatos(distribucion):

    # Estilos para los párrafos

    estilo_celda = styles["BodyText"]
    estilo_celda.wordWrap = 'CJK'  # Para que el texto ajuste automáticamente

    datos = [ ["Materia", "Profesor", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]]
    # Diccionario temporal para almacenar las filas por materia y profesor
    tabla_materias = {}
    
    # Recorrer cada dictado en la distribución
    for dictado, recurso in distribucion.items():
        materia = dictado.comision.materia.nombre
        profesor = dictado.comision.profesor.nombre
        dia = recurso.dia
        horario = recurso.horario
        aula = recurso.aula.nombre
        
        # Crear una clave única para la materia y profesor
        clave = (materia, profesor)
        
        # Si no existe esa clave en tabla_materias, inicializar una fila
        if clave not in tabla_materias:
            tabla_materias[clave] = ["", "", "", "", ""]
        

        tabla_materias[clave][dia] = f"{horario}\nAula {aula}"
    
    # Convertir la tabla de materias en el formato de la tabla final
    for (materia, profesor), horarios in tabla_materias.items():
        datos.append([
            Paragraph(materia, estilo_celda), Paragraph(profesor, estilo_celda),
            horarios[0], horarios[1], horarios[2], horarios[3], horarios[4]
        ])

    return datos
   

# Función para generar el PDF
def crear_pdf(solucion_final, nombre_archivo = "horarios_clase.pdf"):
    
    # Configuración básica del documento
    doc = SimpleDocTemplate(nombre_archivo, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elementos = []
    
   
    # Ancho de cada columna
    page_width = A4[0] - 40  # Ancho de página menos márgenes
    col_widths = [page_width * 0.25, page_width * 0.25] + [page_width * 0.1] * 5

    datos = cargarDatos(solucion_final)

    # Crear la tabla con los nuevos anchos de columna
    tabla = Table(datos, colWidths=col_widths)

    # Estilos de la tabla
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),         # Fondo de la cabecera
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),    # Color del texto de la cabecera
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                # Centrar todo el texto
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),               # Centrar verticalmente
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),      # Negrita en la cabecera
        ('FONTSIZE', (0, 0), (-1, 0), 10),                    # Tamaño de letra de la cabecera
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),                # Espaciado de la cabecera
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),       # Fondo de las celdas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),        # Bordes de las celdas
    ])
    tabla.setStyle(estilo_tabla)


    elementos.append(Paragraph("Distribución de aulas", styles["h1"]))
    elementos.append(tabla)
    elementos.append(Paragraph(f"evaluacion de penalización: {evaluar(solucion_final)}"))

    # Generar el archivo PDF
    doc.build(elementos)
    print(f"PDF generado con éxito en: {nombre_archivo}")


