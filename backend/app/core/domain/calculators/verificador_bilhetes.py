"""
Verificação de bilhetes completos.

PADRÃO GRASP: Information Expert
- VerificadorBilhetes conhece regras de verificação de bilhetes
- Usa PathFinder para lógica de conectividade
"""

from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
from app.core.domain.entities.rota import Rota

if TYPE_CHECKING:
    from .pathfinder import PathFinder


def _get_pathfinder():
    """Lazy import para evitar importação circular."""
    from .pathfinder import PathFinder
    return PathFinder()


@dataclass
class VerificadorBilhetes:
    """
    Information Expert - Verifica bilhetes completos de um jogador.

    Responsabilidades:
    - Verificar se jogador completou bilhete específico
    - Listar todos os bilhetes completos
    - Listar todos os bilhetes incompletos
    - Calcular pontuação de bilhetes

    GRASP Principles:
    - Information Expert: Conhece bilhetes e rotas do jogador
    - Low Coupling: Usa PathFinder para lógica de busca
    - High Cohesion: Focado em verificação de bilhetes
    """

    pathfinder: 'PathFinder' = field(default_factory=lambda: _get_pathfinder())

    def verificar_bilhete_completo(
        self,
        bilhete,
        rotas_conquistadas: List[Rota]
    ) -> bool:
        """
        Verifica se bilhete foi completado.

        Args:
            bilhete: BilheteDestino a verificar
            rotas_conquistadas: Rotas conquistadas pelo jogador

        Returns:
            True se existe caminho entre origem e destino
        """
        return self.pathfinder.verificar_caminho_existe(
            origem=bilhete.cidadeOrigem,
            destino=bilhete.cidadeDestino,
            rotas_conquistadas=rotas_conquistadas
        )

    def listar_bilhetes_completos(
        self,
        bilhetes: List,
        rotas_conquistadas: List[Rota]
    ) -> List:
        """
        Retorna lista de bilhetes completos.

        Args:
            bilhetes: Lista de BilheteDestino do jogador
            rotas_conquistadas: Rotas conquistadas pelo jogador

        Returns:
            Lista de bilhetes completos
        """
        completos = []
        for bilhete in bilhetes:
            if self.verificar_bilhete_completo(bilhete, rotas_conquistadas):
                completos.append(bilhete)
        return completos

    def listar_bilhetes_incompletos(
        self,
        bilhetes: List,
        rotas_conquistadas: List[Rota]
    ) -> List:
        """
        Retorna lista de bilhetes incompletos.

        Args:
            bilhetes: Lista de BilheteDestino do jogador
            rotas_conquistadas: Rotas conquistadas pelo jogador

        Returns:
            Lista de bilhetes incompletos
        """
        incompletos = []
        for bilhete in bilhetes:
            if not self.verificar_bilhete_completo(bilhete, rotas_conquistadas):
                incompletos.append(bilhete)
        return incompletos

    def calcular_pontuacao_bilhetes(
        self,
        bilhetes: List,
        rotas_conquistadas: List[Rota]
    ) -> int:
        """
        Calcula pontuação de bilhetes: +pontos para completos, -pontos para incompletos.

        Args:
            bilhetes: Lista de BilheteDestino do jogador
            rotas_conquistadas: Rotas conquistadas pelo jogador

        Returns:
            Pontuação total de bilhetes
        """
        pontuacao = 0

        for bilhete in bilhetes:
            if self.verificar_bilhete_completo(bilhete, rotas_conquistadas):
                pontuacao += bilhete.pontos
            else:
                pontuacao -= bilhete.pontos

        return pontuacao