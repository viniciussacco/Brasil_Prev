import random

from config.system import INTERVALO_VALOR_PROPRIEDADE, PERCENTUAL_ALUGUEL


class Propriedade():
    valor = 0
    aluguel = 0
    dono = None
    
    def __init__(self) -> None:
        self.valor = random.randrange(INTERVALO_VALOR_PROPRIEDADE[0], INTERVALO_VALOR_PROPRIEDADE[1])
        self.aluguel = round(self.valor * (PERCENTUAL_ALUGUEL/100),2)
    
