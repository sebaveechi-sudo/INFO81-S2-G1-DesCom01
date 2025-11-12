import datetime as dt
from collections.abc import Callable
from typing import Any

from ppdc_timed_generator.generador import Generador

class GeneradorExponencial(Generador):

    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ):
        
        cpm = self.poblacion * 0.2 / self.minutos_de_funcionamiento()
        
        if cpm == 0:
            if update:
                self.current_datetime += dt.timedelta(minutes=minutos)
            return []

        lambda_rate = cpm
        
        clientes = []
        minutos_transcurridos = 0.0
        #bucle
        while True:
            tiempo_hasta_proximo = self.rdm.expovariate(lambda_rate)
            
            minutos_transcurridos += tiempo_hasta_proximo
            
            if minutos_transcurridos > minutos:
                break
                
            id_cliente = self.rdm.randint(0, self.poblacion - 1) 
            
            tiempo_llegada_exacta = self.current_datetime + dt.timedelta(minutes=minutos_transcurridos)
            
            cliente = constructor(id_cliente, tiempo_llegada_exacta)
            clientes.append(cliente)
        # act. reloj principal
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)
            
        return clientes
