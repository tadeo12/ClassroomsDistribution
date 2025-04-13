from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def loadData(allocation):
    cellStyle = styles["BodyText"]
    cellStyle.wordWrap = 'CJK'

    data = [["Materia", "Profesor", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]]
    table = {}
    
    for resource, commission in allocation.items():
        if commission is not None:
            subject = commission.subject.name
            teacher = commission.teacher.name
            day = resource.day
            hour = resource.hour
            classroom = resource.classroom.name
            key = (commission.name, subject, teacher)
            if key not in table:
                table[key] = ["", "", "", "", ""]
            table[key][day] = f"{hour}<br/>{classroom}" 
    
    for (commission, subject, teacher), schedules in table.items():
        data.append([
            Paragraph(subject, cellStyle), 
            Paragraph(teacher, cellStyle),
            Paragraph(schedules[0], cellStyle), 
            Paragraph(schedules[1], cellStyle),
            Paragraph(schedules[2], cellStyle), 
            Paragraph(schedules[3], cellStyle),
            Paragraph(schedules[4], cellStyle)
        ])

    return data

def createPdf(allocation, fileName = "horarios_clase.pdf"):
    doc = SimpleDocTemplate(fileName, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = []
    
    pageWidth = A4[0] - 40
    table = generateTable(allocation, pageWidth)

    elements.append(Paragraph("Distribución de aulas", styles["h1"]))
    elements.append(table)
    #elements.append(Paragraph(f"evaluacion de penalización: {evaluar(solucion_final)}"))
    doc.build(elements)
    print(f"PDF generado con éxito en: {fileName}")


def generateTable(allocation, pageWidth):
    colWidths = [pageWidth * 0.2, pageWidth * 0.2] + [pageWidth * 0.12] * 5

    data = loadData(allocation)

    table = Table(data, colWidths)
    styleTable= TableStyle([
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
    table.setStyle(styleTable)

    return table