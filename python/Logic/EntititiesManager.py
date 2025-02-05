from Models.Place import Place
from Models.Commission import Commission
from Models.Career import Career
from Models.Classroom import Classroom
from Models.Resource import Resource
from Models.Semester import Semester
from Models.Teacher import Teacher
from Models.Subject import Subject


import json
from typing import List

from .ResourcesGenerator import generateResources

def createEntitiesFromJson(json_data):
    if isinstance(json_data, str): 
        data = json.loads(json_data)
    else:  
        data = json_data  # Si ya es un diccionario, úsalo directamente

    places = [Place(p['name']) for p in data.get('places', [])]
    places_dict = {p.name: p for p in places}
    
    teachers = [Teacher(t['name']) for t in data.get('teachers', [])]
    teachers_dict = {t.name: t for t in teachers}
    
    subjects = [Subject(s['name']) for s in data.get('subjects', [])]
    subjects_dict = {s.name: s for s in subjects}
    
    classrooms = [Classroom(c['name'], c['capacity'], places_dict[c['place']]) for c in data.get('classrooms', [])]
    classrooms_dict = {c.name: c for c in classrooms}
    
    semesters = []
    semesters_dict = {}
    for s in data.get('semesters', []):
        semester_subjects = [subjects_dict[sub] for sub in s.get('subjects', [])]
        semester = Semester(s['semester_name'], semester_subjects)
        semesters.append(semester)
        semesters_dict[s['semester_name']] = semester
    
    careers = []
    careers_dict = {}
    for c in data.get('careers', []):
        career_semesters = [semesters_dict[sem] for sem in c.get('semesters', [])]
        career = Career(c['name'], career_semesters)
        careers.append(career)
        careers_dict[c['name']] = career
    
    commissions = []
    for co in data.get('commissions', []):
        career_list = [careers_dict[car] for car in co.get('careers', [])]
        commission = Commission(co['name'], teachers_dict[co['teacher']], subjects_dict[co['subject']], co['students'], career_list, co.get('hoursPerWeek', 8))
        commissions.append(commission)

    Resource._counter = 0     
    resources = generateResources(classrooms)
    
    return {
        'places': places,
        'teachers': teachers,
        'subjects': subjects,
        'classrooms': classrooms,
        'semesters': semesters,
        'careers': careers,
        'commissions': commissions,
        'resources': resources
    }

