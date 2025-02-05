from typing import List
import random
from ConfigurationVars import *  
from Models.Commission import Commission
from Models.Resource import Resource


def generateRandomInitialAllocation(commissions: List[Commission], resources: List[Resource]):
    allocation = {}
    available_resources = resources.copy()  # Hacemos una copia para gestionar los recursos disponibles

    for commission in commissions:
        required_blocks = int(commission.hours / HOURS_PER_RESOURCE)

        for _ in range(required_blocks):
            if not available_resources:
                raise ValueError("No hay suficientes recursos disponibles para asignar las comisiones.")
            
            # Elegir un recurso aleatorio y asignarlo
            selected_resource = random.choice(available_resources)
            available_resources.remove(selected_resource)
            allocation[selected_resource] = commission

    return allocation