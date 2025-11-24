"""
Constantes centralizadas do jogo Ticket to Ride Brasil.

Este módulo centraliza todas as constantes do jogo para:
- Evitar duplicação de valores
- Facilitar manutenção e ajustes de regras
- Garantir consistência entre componentes
- Seguir o princípio DRY (Don't Repeat Yourself)

GRASP Principles:
- Pure Fabrication: Módulo criado para centralizar constantes
- Protected Variations: Encapsula regras do jogo em um único lugar
- Low Coupling: Componentes dependem de constantes, não de valores mágicos
"""

from typing import Dict

# ============================================================================
# PONTUAÇÃO
# ============================================================================

# Tabela de pontuação por comprimento de rota
# Baseada nas regras oficiais do Ticket to Ride
TABELA_PONTOS_ROTA: Dict[int, int] = {
    1: 1,   # Rota de 1 vagão = 1 ponto
    2: 2,   # Rota de 2 vagões = 2 pontos
    3: 4,   # Rota de 3 vagões = 4 pontos
    4: 7,   # Rota de 4 vagões = 7 pontos
    5: 10,  # Rota de 5 vagões = 10 pontos
    6: 15,  # Rota de 6 vagões = 15 pontos
}

# Bônus para o jogador com o caminho contínuo mais longo
BONUS_MAIOR_CAMINHO: int = 10

# ============================================================================
# CONFIGURAÇÃO INICIAL DO JOGO
# ============================================================================

# Número de cartas de vagão que cada jogador recebe no início
CARTAS_INICIAIS: int = 4

# Número de vagões (trens) que cada jogador possui no início
TRENS_INICIAIS: int = 45

# Número de cartas abertas visíveis na mesa durante o jogo
CARTAS_ABERTAS_MESA: int = 5

# ============================================================================
# BILHETES DE DESTINO - ESCOLHA INICIAL
# ============================================================================

# Número mínimo de bilhetes que o jogador DEVE manter na escolha inicial
BILHETES_INICIAIS_MIN: int = 2

# Número máximo de bilhetes que o jogador PODE manter na escolha inicial
# (Equivale ao número de bilhetes sorteados: 3)
BILHETES_INICIAIS_MAX: int = 3

# ============================================================================
# BILHETES DE DESTINO - COMPRA DURANTE O JOGO
# ============================================================================

# Número de bilhetes sorteados quando jogador compra durante a partida
BILHETES_COMPRA_SORTEADOS: int = 3

# Número mínimo de bilhetes que o jogador DEVE manter ao comprar durante jogo
BILHETES_COMPRA_MIN: int = 1

# ============================================================================
# CONDIÇÃO DE FIM DE JOGO
# ============================================================================

# Jogo entra em última rodada quando um jogador tem este número ou menos de vagões
TRENS_ULTIMA_RODADA: int = 2
