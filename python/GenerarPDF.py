from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

# Función para generar el PDF
def crear_pdf():
    # Nombre del archivo de salida
    archivo_pdf = "horarios_clases.pdf"
    
    # Configuración básica del documento
    doc = SimpleDocTemplate(archivo_pdf, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elementos = []
    
    # Estilos para los párrafos
    styles = getSampleStyleSheet()
    estilo_celda = styles["BodyText"]
    estilo_celda.wordWrap = 'CJK'  # Para que el texto ajuste automáticamente
    
    # Datos de ejemplo con texto largo para probar el ajuste
    datos = [
        ["Materia", "Profesor", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
        [Paragraph("Resolución de Problemas y Algoritmos", estilo_celda), Paragraph("Dra. Jesica Carballido", estilo_celda), "8-12", "", "8-12", "", ""],
        [Paragraph("Teoría de la Computabilidad", estilo_celda), Paragraph("Dr. Carlos Chesñevar", estilo_celda), "8-12", "", "8-12", "", ""],
        [Paragraph("Estructuras de Datos", estilo_celda), Paragraph("Dr. Sergio Gómez", estilo_celda), "", "", "14-18", "", ""],
    ]
    
    # Ancho de cada columna
    page_width = A4[0] - 40  # Ancho de página menos márgenes
    col_widths = [page_width * 0.25, page_width * 0.25] + [page_width * 0.1] * 5

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

    # Generar el archivo PDF
    doc.build(elementos)
    print(f"PDF generado con éxito en: {archivo_pdf}")

# Llamada a la función para generar el PDF
crear_pdf()
