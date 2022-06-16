import random
from enum import Enum

from config.system import GANHO_VOLTA_COMPLETA, QTDE_PROPRIEDADES


class Perfil(Enum):
    IMPULSIVO = 'Impulsivo'
    EXIGENTE = 'Exigente'
    CAUTELOSO = 'Cauteloso'
    ALEATORIO = 'Aleatório'

class Estado(Enum):
    ATIVO = True
    ELIMINADO = False

class Player():
    perfil = None
    caixa = 0
    estado = Estado.ATIVO
    posicao = -1

    #Construtor para objeto player
    def __init__(self, perfil, caixa = 300) -> None:
        self.perfil = perfil
        self.caixa = caixa

    #Executa o movimento do jogador
    def andar(self, quantidade_casas):
        posicao_futura = self.posicao + quantidade_casas

        if (posicao_futura + 1) > QTDE_PROPRIEDADES:
            self.caixa += GANHO_VOLTA_COMPLETA
            posicao_futura = posicao_futura - QTDE_PROPRIEDADES

        self.posicao = posicao_futura

    #Calcula o valor a ser pago pelo aluguel
    def desconta_aluguel(self, valor_aluguel):
        #Caso tenha caixa, paga o aluguel
        if valor_aluguel < self.caixa:
            self.caixa -= valor_aluguel
            return valor_aluguel
        #Caso não tenha caixa, paga o saldo possivel e elimina o jogador
        else:
            aluguel = self.caixa
            self.caixa = 0
            self.estado = Estado.ELIMINADO

            return  aluguel

    #executa a jogada
    def efetuar_jogada(self, propriedade):
        if not propriedade.dono and propriedade.valor < self.caixa:
            match self.perfil:
                case Perfil.IMPULSIVO:                    
                    #Se a propriedade estiver dentro do valor de compra adquire.                
                    propriedade.dono = self
                    self.caixa -= propriedade.valor                                          

                case Perfil.EXIGENTE:
                    #Se a propriedade estiver dentro do valor de compra e aluguel acima de 50 adquire.
                    if propriedade.aluguel > 50:
                       propriedade.dono = self
                       self.caixa -= propriedade.valor

                case Perfil.CAUTELOSO:    
                    #Se a propriedade estiver dentro do valor de compra e aluguel acima de 50 adquire.
                    if (self.caixa - propriedade.valor) >= 80:
                        propriedade.dono = self
                        self.caixa -= propriedade.valor

                case Perfil.ALEATORIO:
                    #50% de chance, obtido de forma aleatória de comprar
                    if  random.randint(0,1) == 1:
                        propriedade.dono = self
                        self.caixa -= propriedade.valor

        #Caso propriedade já tenha dono                 
        elif propriedade.dono:
            if propriedade.dono.estado == Estado.ATIVO and propriedade.dono != self:
                propriedade.dono.caixa += self.desconta_aluguel(propriedade.aluguel) 
