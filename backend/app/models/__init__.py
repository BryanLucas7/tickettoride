# backend/app/models/__init__.py
# Expor módulos principais
from .entities.jogo import Jogo
from .entities.jogador import Jogador
from .entities.carta import Carta
from .entities.carta_vagao import CartaVagao
from .entities.bilhete_destino import BilheteDestino
from .entities.mao import Mao
from .entities.baralho import Baralho
from .managers.gerenciador_de_baralho import GerenciadorDeBaralho
from .managers.gerenciador_de_turnos import GerenciadorDeTurnos
from .calculators.placar import Placar
from .entities.cidade import Cidade
from .entities.rota import Rota
from .entities.tabuleiro import Tabuleiro
from .entities.cor import Cor
