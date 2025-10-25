from typing import List 
from app.Models.Classroom import Classroom
from app.Models.Resource import Resource
from ConfigManager import ConfigManager

def generateResources(classrooms: List[Classroom], classroomsAvailability) -> list:
    config = ConfigManager().getConfig()
    hoursPerDay = config["hours_per_day"]
    hoursPerResource = config["hours_per_resource"]
    daysPerWeek = config["days_per_week"]

    resources = []
    slotsPerDay = int(hoursPerDay / hoursPerResource)

    for classroom in classrooms:
        available_slots = classroomsAvailability.get(classroom)
        allowAll = not available_slots 
        for day in range(daysPerWeek):
            for slot in range(slotsPerDay):
                if allowAll or (day, slot) in available_slots:
                    resource = Resource(classroom, day, slot)
                    resources.append(resource)

    return resources

