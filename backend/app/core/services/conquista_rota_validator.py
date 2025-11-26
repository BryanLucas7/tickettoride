"""
Validador de conquista de rotas.

PADRÃO GRASP: Pure Fabrication
- ConquistaRotaValidator encapsula todas as validações de conquista
- Separa lógica de validação do controller
"""

from typing import List, Dict
from ..domain.entities.jogador import Jogador
from ..domain.entities.rota import Rota
from ..domain.entities.carta_vagao import CartaVagao
from ..domain.strategies.rota_validation_factory import criar_estrategia_validacao
from ..domain.strategies.rota_dupla_validator import RotaDuplaValidator
from ..domain.support.responses import success_response, error_response


class ConquistaRotaValidator:
    """
    Pure Fabrication - Valida todas as condições para conquista de rota.

    Responsabilidades:
    - Validar disponibilidade da rota
    - Validar cartas do jogador (Strategy Pattern)
    - Validar regras de rotas duplas
    - Retornar resultados de validação padronizados

    GRASP Principles:
    - Pure Fabrication: Classe criada para responsabilidade específica
    - Information Expert: Conhece regras de validação
    - Low Coupling: Não depende de outros serviços
    - High Cohesion: Focado apenas em validações
    """

    def __init__(self, validador_duplas: RotaDuplaValidator = None):
        """
        Inicializa o validador.

        Args:
            validador_duplas: Validador de rotas duplas (opcional)
        """
        self.validador_duplas = validador_duplas

    def validar_conquista(
        self,
        jogador: Jogador,
        rota: Rota,
        cartas_usadas: List[CartaVagao]
    ) -> Dict:
        """
        Executa todas as validações para conquista de rota.

        Args:
            jogador: Jogador que quer conquistar
            rota: Rota alvo
            cartas_usadas: Cartas que serão usadas

        Returns:
            Dict com resultado da validação
        """
        # 1. Validar disponibilidade da rota
        if rota.proprietario is not None:
            return self._erro("❌ Rota já foi conquistada por outro jogador!")

        # 2. Validar cartas (Strategy Pattern)
        estrategia = criar_estrategia_validacao(rota.cor)
        resultado_validacao = estrategia.validar(
            cartas_jogador=cartas_usadas,
            comprimento=rota.comprimento,
            cor_rota=rota.cor
        )

        if not resultado_validacao['valido']:
            return self._erro(f"❌ Cartas inválidas: {resultado_validacao['mensagem']}")

        # 3. Validar regra de rotas duplas
        if self.validador_duplas:
            resultado_dupla = self.validador_duplas.validar_conquista_rota(rota=rota, jogador=jogador)

            if not resultado_dupla['valido']:
                return self._erro(f"❌ {resultado_dupla['mensagem']}")

        return success_response("Validação bem-sucedida")

    def _erro(self, mensagem: str) -> Dict:
        """Retorna dicionário de erro padronizado"""
        return error_response(mensagem)