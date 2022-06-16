import argparse
import random

from config.system import LIMITE_RODADAS, QTDE_PROPRIEDADES
from Logger import Logger
from players import Estado, Perfil, Player
from propriedades import Propriedade


#========================= ROTINAS ==========================================
# Efetua a partida
def executa_partida(players, tabuleiro):
    logger.debug('Começando nova partida...\n')
    rodada = 0
    while rodada < LIMITE_RODADAS:
        rodada += 1
        logger.debug(f'Rodada nro {rodada}...\n')
        
        #Executa rodada para um player
        player_nro = -1
        while player_nro < len(players) - 1:
            player_nro += 1

            #Obtem o player da vez
            player = players[player_nro]

            if player.estado == Estado.ATIVO:
                #Rola o dado
                nro_passos = random.randint(1,6)
                logger.debug(f"Player nro {player_nro}, Perfil {player.perfil} anda {nro_passos} passos...")

                #Movimenta e efetua jogada
                player.andar(nro_passos)
                logger.debug(f"Propriedade {player.posicao} => valor {tabuleiro[player.posicao].valor}, Aluguel {tabuleiro[player.posicao].aluguel}...")

                player.efetuar_jogada(tabuleiro[player.posicao])

                logger.debug(f"Situação do player nro {player_nro} após rodada => Caixa {round(player.caixa,2)} Estado {player.estado}...\n")

        if not len(list(filter(lambda p: p.estado == Estado.ATIVO, players))) > 1:                         
            break
    
    #Processa Vencedor
    resultado = {"qtde_turnos":rodada}

    #Ordena por caixa em caso de empate mantém a ordem original, filtra os ativos
    list_ativos = list(filter(lambda p: p.estado == Estado.ATIVO, sorted(players, key=lambda x: x.caixa, reverse=True)))

    resultado['ganhador'] = list_ativos[0].perfil

    #Partida acabou por timeout
    if len(list_ativos) > 1:
        resultado['timeout'] = True
    else:    
        resultado['timeout'] = False

    return resultado

#Gera estatísticas da execução
def gerar_estatisticas(resultados):
    qtde_timeout = 0
    total_turnos = 0

    sumarizacao_perfil = {
        Perfil.ALEATORIO : 0,
        Perfil.CAUTELOSO : 0,
        Perfil.EXIGENTE : 0,
        Perfil.IMPULSIVO :0
    }

    #Executa sumarizações
    for res in resultados:
        if res['timeout']:
            qtde_timeout += 1

        sumarizacao_perfil[res['ganhador']] += 1
        total_turnos += res['qtde_turnos']

    perfil_vencedor = None
    
    tmp_value = -1
    for i in sumarizacao_perfil:
        if sumarizacao_perfil[i] > tmp_value:
            perfil_vencedor = i.value
            tmp_value = sumarizacao_perfil[i]

    logger.info('============ CONTABILIZACAO ===================')
    logger.info(f'TOTAL DE TURNOS............. {total_turnos}')
    logger.info(f'MEDIA DE TURNOS POR PARTIDA. {round(total_turnos/len(resultados),2)}')
    logger.info(f'QTDE DE TIMEOUTS............ {qtde_timeout}')
    logger.info(f'-------- PERCENTUAL DE VITORIAS --------------')
    logger.info(f'IMPULSIVO................... {round(sumarizacao_perfil[Perfil.IMPULSIVO]/len(resultados) * 100,2)}')
    logger.info(f'EXIGENTE.................... {round(sumarizacao_perfil[Perfil.EXIGENTE]/len(resultados) * 100,2)}')
    logger.info(f'CAUTELOSO................... {round(sumarizacao_perfil[Perfil.CAUTELOSO]/len(resultados) * 100,2)}')
    logger.info(f'ALEATORIO................... {round(sumarizacao_perfil[Perfil.ALEATORIO]/len(resultados) * 100,2)}')
    logger.info(f'PERFIL COM MAIS VITORIAS.... {perfil_vencedor}')

#========================================== EXECUCAO ===============================================
# Configura os parametros da linha de comando
parser = argparse.ArgumentParser()

#Argumento do arquivo de mailing
parser.add_argument(
    "-s",
    "--simulacoes",
    default=300,
    help=(
        "Numero de simulações que devem ser rodadas"
        "Example --simulacoes 1000, default=300"
    ),   
)

#Argumento do log
parser.add_argument(
    "-log",
    "--log",
    default="info",
    help=(
        "Provide logging level. "
        "Example --log debug', default='warning'"),
)

#Logger para conferência
logger = Logger(parser).logger

#Variaveis da simulação
rodadas = 0
simulacoes = int(parser.parse_args().simulacoes)
simulacao = 0
lista_resultados =[]

#inicia as simulações
while simulacao < simulacoes: 
    simulacao += 1

    #Cria um Tabuleiro
    tabuleiro = []
    count = 0
    while count < QTDE_PROPRIEDADES:
        tabuleiro.append(Propriedade())
        count += 1

    #Cria e Embaralha a Ordem dos players
    players = [Player(Perfil.IMPULSIVO), Player(Perfil.EXIGENTE), Player(Perfil.CAUTELOSO), Player(Perfil.ALEATORIO)]
    random.shuffle(players)

    #Executa as partidas
    lista_resultados.append(executa_partida(players, tabuleiro))

gerar_estatisticas(lista_resultados)
