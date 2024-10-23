import random
import math
from Models import *

class SimulatedAnnealing:
    def __init__(self, aulas, comisiones, dias, franjas_horarias):
        self.aulas = aulas
        self.comisiones = comisiones
        self.dias = dias
        self.franjas_horarias = franjas_horarias

        self.recursos = [] #lista de recursos, con un boolean para representar si esta ocupado o no

        for aula in self.aulas:
            for dia in self.dias:
                for horario in self.franjas_horarias:
                    self.recursos.append({'recurso': Recurso(aula, dia, horario), 'ocupado': False})

        self.distribucion_actual = self.generar_distribucion_inicial()
    
  
        
    def generar_bloque_4_horas(self):
        """Generar un bloque de 4 horas (2 franjas horarias consecutivas) que no esté ocupado"""
        while True:
            dia = random.choice(self.dias)
            aula = random.choice(self.aulas)
            idx_franja = random.randint(0, len(self.franjas_horarias) - 2)  # Asegurar franjas consecutivas
            
            # Verificar si ambas franjas consecutivas están disponibles
            recurso1 = next((r for r in self.recursos if r['recurso'].aula == aula and r['recurso'].dia == dia and r['recurso'].horario == self.franjas_horarias[idx_franja]), None)
            recurso2 = next((r for r in self.recursos if r['recurso'].aula == aula and r['recurso'].dia == dia and r['recurso'].horario == self.franjas_horarias[idx_franja + 1]), None)
            
            if recurso1 and recurso2 and not recurso1['ocupado'] and not recurso2['ocupado']:
                # Marcar los recursos como ocupados
                recurso1['ocupado'] = True
                recurso2['ocupado'] = True
                return [recurso1['recurso'], recurso2['recurso']]    
    
    def generar_distribucion_inicial(self):
        """Generar la distribución inicial donde cada comisión tiene 2 bloques de 4 horas (total 4 recursos)"""
        distribucion = {}
        for comision in self.comisiones:
            recursos = []
            # Generar dos bloques de 4 horas
            recursos.extend(self._generar_bloque_4_horas())  # Primer bloque de 4 horas
            recursos.extend(self._generar_bloque_4_horas())  # Segundo bloque de 4 horas
            distribucion[comision] = recursos
        return distribucion
    
    def calcular_costo(self, distribucion):
        # Función que deberás personalizar según tus restricciones
        costo = 0
        for recurso in distribucion:
            if recurso.aula.capacidad < recurso.comision.cant_alumnos:
                costo += 10  # Penalización por sobrepasar la capacidad del aula
            # Puedes agregar más restricciones aquí, como evitar solapamientos
        return costo
    
    def generar_vecino(self):
        # Generar una nueva distribución modificando ligeramente la actual
        nueva_distribucion = self.distribucion_actual.copy()
        idx = random.randint(0, len(nueva_distribucion) - 1)
        nueva_distribucion[idx].aula = random.choice(self.aulas)
        nueva_distribucion[idx].dia = random.choice(self.dias)
        nueva_distribucion[idx].horario = random.choice(self.franjas_horarias)
        return nueva_distribucion
    
    def recocido_simulado(self, temperatura_inicial, tasa_enfriamiento, temperatura_minima):
        temperatura = temperatura_inicial
        
        while temperatura > temperatura_minima:
            nueva_distribucion = self.generar_vecino()
            costo_actual = self.calcular_costo(self.distribucion_actual)
            nuevo_costo = self.calcular_costo(nueva_distribucion)
            
            if nuevo_costo < costo_actual:
                self.distribucion_actual = nueva_distribucion
            else:
                probabilidad_aceptacion = math.exp(-(nuevo_costo - costo_actual) / temperatura)
                if random.random() < probabilidad_aceptacion:
                    self.distribucion_actual = nueva_distribucion
            
            # Enfriar la temperatura
            temperatura *= tasa_enfriamiento
        
        return self.distribucion_actual
