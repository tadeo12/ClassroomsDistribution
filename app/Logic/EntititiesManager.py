import logging
from app.Models.Place import Place
from app.Models.Commission import Commission
from app.Models.Classroom import Classroom
from app.Models.Resource import Resource
from app.Models.Teacher import Teacher
from app.Models.Subject import Subject
import json
from app.Models.Group import Group
from app.Logic.ResourcesGenerator import generateResources

def createEntitiesFromJson(json_data):
    if isinstance(json_data, str): 
        data = json.loads(json_data)
    else:  
        data = json_data


    logging.info(f"DATA: '{data}'.")

    places = [Place(place_data['name']) for place_data in data['places']]
    places_dictionary = {place.name: place for place in places}

    teachers = [Teacher(teacher_data['name']) for teacher_data in data['teachers']]
    teachers_dictionary = {teacher.name: teacher for teacher in teachers}

    subjects = [Subject(subject_data['name']) for subject_data in data['subjects']]
    subjects_dictionary = {subject.name: subject for subject in subjects}

    classrooms = [
        Classroom(classroom_data['name'], classroom_data['capacity'], places_dictionary[classroom_data['place']])
        for classroom_data in data['classrooms']
    ]

    groups = [Group(group_data['name']) for group_data in data['groups']]
    groups_dictionary = {group.name: group for group in groups}

    commissions = [
        Commission(
            commission_data['name'], 
            teachers_dictionary[commission_data['teacher']], 
            subjects_dictionary[commission_data['subject']], 
            commission_data['students'], 
            commission_data.get('hoursPerWeek', 8)
        ) for commission_data in data['commissions']
    ]
    commissions_dictionary = {commission.name: commission for commission in commissions}

    for relation in data['commissions_groups']:
        commission = commissions_dictionary[relation['commission']]
        group = groups_dictionary[relation['group']]
        if group not in commission.groups:
            commission.groups.append(group)
        if commission not in group.commissions:
            group.commissions.append(commission)

    Resource._counter = 0     
    resources = generateResources(classrooms)

    return {
        'places': places,
        'teachers': teachers,
        'subjects': subjects,
        'classrooms': classrooms,
        'commissions': commissions,
        'groups': groups,
        'resources': resources
    }