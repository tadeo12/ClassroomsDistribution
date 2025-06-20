from typing import List
from ConfigurationVars import *
from app.Models.Classroom import Classroom
from app.Models.Resource import Resource

def generateResources(classrooms: List[Classroom]) -> list:
    resources = []
    slotsPerDay= int(HOURS_PER_DAY / HOURS_PER_RESOURCE)
    for classroom in classrooms:
        for day in range(DAYS_PER_WEEK):
            for slot in range(slotsPerDay):
                resource = Resource(classroom, day, slot)
                resources.append(resource)
    return resources

