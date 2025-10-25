import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from ConfigManager import ConfigManager
from app.GUI.Graphs import generateFiguresForPdf
import streamlit as st


styles = getSampleStyleSheet()

def groupByClassroom(allocation):
    grouped = {}
    for resource, commission in allocation.items():
        if commission is not None:
            classroom = resource.classroom.name
            if classroom not in grouped:
                grouped[classroom] = {}
            grouped[classroom][resource] = commission
    return grouped



def loadClassroomScheduleData(allocation):
    cellStyle = styles["BodyText"]
    cellStyle.wordWrap = 'CJK'

    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    # Detectar los índices de hora presentes
    used_hour_indices = sorted(set(resource.hour for resource in allocation))
    schedule = {}

    for idx in used_hour_indices:
        real_hour = idx + 8  # Ahora 0 → 8, 1 → 9, ..., 13 → 21
        for day in range(5):
            schedule[(real_hour, day)] = []

    for resource, commission in allocation.items():
        if commission is not None:
            day = resource.day
            real_hour = resource.hour + 8
            info = f"{commission.name} - {commission.subject.name} - {commission.teacher.name}"
            schedule[(real_hour, day)].append(info)

    data = [["Hora"] + days]

    real_hours_sorted = sorted(set(h for (h, _) in schedule))

    for hour in real_hours_sorted:
        row = [Paragraph(f"{hour}:00", cellStyle)]
        for day in range(5):
            entries = schedule.get((hour, day), [])
            content = "<br/>".join(entries)
            row.append(Paragraph(content, cellStyle))
        data.append(row)

    return data

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

def generateClassroomTable(allocation, pageWidth):
    colWidths = [pageWidth * 0.1] + [pageWidth * 0.18] * 5  # Hora + 5 días

    data = loadClassroomScheduleData(allocation)

    table = Table(data, colWidths)
    styleTable = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(styleTable)

    return table

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

def createPdf(allocation, fileName = "horarios_clase.pdf"):
    doc = SimpleDocTemplate(fileName, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = []
    
    pageWidth = A4[0] - 40
    

    elements.append(Paragraph("Distribución de aulas", styles["h1"]))
    table = generateTable(allocation, pageWidth)
    elements.append(table)
    #elements.append(Paragraph(f"evaluacion de penalización: {evaluar(solucion_final)}"))

    grouped_alloc = groupByClassroom(allocation)
    for classroom, alloc in grouped_alloc.items():
        elements.append(Paragraph(f"Aula: {classroom}", styles["Heading2"]))
        table = generateClassroomTable(alloc, pageWidth)
        elements.append(table)
        elements.append(Paragraph("<br/><br/>", styles["BodyText"]))  


    config = ConfigManager().getConfig()
    elements.append(Paragraph("Informacion de ejecucion del algoritmo", styles["h1"]))
    elements.append(Paragraph("Configuraciones: ", styles["h2"]))
    for key, value in config.items():
        elements.append(Paragraph(f"<b>{key}</b>: {value}", styles["BodyText"]))
        elements.append(Spacer(1, 20))


    # Agregar gráficos una sola vez al final
    if "statsHistory" in st.session_state and st.session_state.statsHistory:
        figures = generateFiguresForPdf(st.session_state.statsHistory)
        elements.append(Paragraph("Estadísticas del algoritmo", styles["h2"]))

        # convertir buffers en objetos Image con tamaño uniforme
        imgs = [Image(buf, width=250, height=180) for buf in figures]

        # armar la tabla de a dos imágenes por fila
        rows = [imgs[i:i+2] for i in range(0, len(imgs), 2)]
        table = Table(rows, colWidths=[260, 260])  # ajustar ancho de columna
        table.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ]))

        elements.append(table)


    # Agregar evaluación al PDF
    if "evaluation" in st.session_state and st.session_state.evaluation:
        elements.append(Paragraph("Evaluación de restricciones", styles["h1"]))
        eval_json = json.dumps(st.session_state.evaluation, indent=4, ensure_ascii=False)
        for line in eval_json.splitlines():
            elements.append(Paragraph(line.replace(" ", "&nbsp;"), styles["Code"]))

    doc.build(elements)
    print(f"PDF generado con éxito en: {fileName}")

