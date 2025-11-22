"""
PADRÃO GRASP: Pure Fabrication
- ConquistaRotaPreview é uma classe fabricada puramente para preview
- Não representa entidade de negócio, apenas utilitário

PADRÃO GRASP: Indirection
- Separa cálculo de preview da lógica de execução
- Cliente pode consultar sem executar ação

Responsabilidades:
- Calcular preview de conquista antes da execução
- Validar condições sem efeitos colaterais
- Fornecer informações para UI
"""

from dataclasses import dataclass
from typing import List, Dict
from ..entities.rota import Rota
from ..entities.carta_vagao import CartaVagao
from ..calculators.calculadora_pontos_rota import CalculadoraPontosRota
from ..strategies.rota_validation_strategy import criar_estrategia_validacao


@dataclass
class ConquistaRotaPreview:
    """
    Serviço para preview de conquista (antes de confirmar).

    Útil para UI mostrar informações antes do jogador confirmar.
    """

    @staticmethod
    def calcular_preview(
        rota: Rota,
        cartas_disponiveis: List[CartaVagao],
        trens_disponiveis: int
    ) -> Dict:
        """
        Calcula preview de conquista de rota.

        Args:
            rota: Rota a ser conquistada
            cartas_disponiveis: Cartas disponíveis na mão do jogador
            trens_disponiveis: Trens disponíveis do jogador

        Returns:
            Dicionário com:
            - pode_conquistar: bool
            - cartas_necessarias: int
            - trens_necessarios: int
            - pontos_potenciais: int
            - opcoes_cartas: List de combinações válidas
            - mensagem: str explicativa
        """
        comprimento = rota.comprimento
        pontos = CalculadoraPontosRota.calcular_pontos(comprimento)

        # Verificar trens
        pode_por_trens = trens_disponiveis >= comprimento

        # Verificar cartas (simplificado - apenas contar por cor)
        estrategia = criar_estrategia_validacao(rota.cor)

        # Tentar validar com cartas disponíveis
        resultado_validacao = estrategia.validar(
            cartas_jogador=cartas_disponiveis[:comprimento],
            comprimento=comprimento,
            cor_rota=rota.cor
        )

        pode_conquistar = pode_por_trens and resultado_validacao['valido']

        mensagem = ""
        if not pode_por_trens:
            mensagem = f"❌ Trens insuficientes (tem {trens_disponiveis}, precisa {comprimento})"
        elif len(cartas_disponiveis) < comprimento:
            mensagem = f"❌ Cartas insuficientes (tem {len(cartas_disponiveis)}, precisa {comprimento})"
        else:
            mensagem = f"✅ Pode conquistar! {comprimento} cartas, {comprimento} trens → +{pontos} pontos"

        return {
            "pode_conquistar": pode_conquistar,
            "cartas_necessarias": comprimento,
            "trens_necessarios": comprimento,
            "pontos_potenciais": pontos,
            "mensagem": mensagem,
            "detalhes": {
                "rota_id": rota.id,
                "cidadeA": rota.cidadeA.nome,
                "cidadeB": rota.cidadeB.nome,
                "cor": rota.cor.value,
                "comprimento": comprimento
            }
        }