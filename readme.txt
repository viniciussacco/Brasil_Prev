- Instalar as dependencias.

Configurar propriedades no arquivo config/system.py

PERCENTUAL_ALUGUEL => Propriedade que define o percentual aplicado para cálculo do valor do aluguel.

INTERVALO_VALOR_PROPRIEDADE => Lista contendo o valor mínimo e valor máximo das propriedades

QTDE_PROPRIEDADES => Tamanho do tabuleiro

LIMITE_RODADAS => Limite de rodadas para finalizar a simulação por timeout

GANHO_VOLTA_COMPLETA => Valor acrescentado ao Player após uma volta completa no tabuleiro.


- Rodar o comando "python simulacao.py"

Caso queira acompanhar o trace da aplicação, rodar o comando python simulacao.py --log debug

Caso queira definir uma quantidade de simulações rodar o comando python simulacao.py --simulacoes <int>

