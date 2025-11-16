from enum import Enum

class Cor(Enum):
    # Cores de cartas (usadas pelo frontend)
    VERMELHO = "vermelho"
    AZUL = "azul"
    VERDE = "verde"
    AMARELO = "amarelo"
    PRETO = "preto"
    LARANJA = "laranja"
    ROXO = "roxo"
    BRANCO = "branco"
    LOCOMOTIVA = "locomotiva"
    
    # Cor especial para rotas (aceita qualquer cor de carta)
    CINZA = "cinza"

