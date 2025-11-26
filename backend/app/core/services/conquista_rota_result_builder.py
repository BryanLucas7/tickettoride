"""
Construtor de resultados para conquista de rotas.

PADRÃO GRASP: Pure Fabrication
- ConquistaRotaResultBuilder constrói respostas padronizadas
- Separa lógica de formatação do controller

Responsabilidades (SRP - focado apenas em construção):
- Construir mensagens de sucesso
- Montar resposta final padronizada

NOTA: Cálculos de pontos e verificação de fim de jogo foram
extraídos para quem chama (Separation of Concerns).
"""

from typing import Dict, Optional
from dataclasses import dataclass
from ..domain.entities.jogador import Jogador
from ..domain.entities.rota import Rota
from ..domain.support.responses import success_response, error_response


@dataclass
class DadosConquista:
    """
    Dados pré-calculados para construção do resultado.
    
    Separa responsabilidade: quem chama calcula, builder apenas monta.
    """
    pontos: int
    cartas_descartadas: int
    trens_removidos: int
    trens_restantes: int
    fim_de_jogo_ativado: bool = False
    alerta_fim: Optional[str] = None
    rota_dupla_bloqueada: bool = False


class ConquistaRotaResultBuilder:
    """
    Pure Fabrication - Constrói resultados padronizados para conquista de rotas.

    Responsabilidades (SRP - apenas construção de resultados):
    - Construir mensagens de sucesso formatadas
    - Montar resposta final padronizada

    GRASP Principles:
    - Pure Fabrication: Classe criada para responsabilidade específica
    - Information Expert: Conhece formato das respostas
    - High Cohesion: Focado APENAS em construção de resultados
    
    NOTA: Cálculos (pontos, fim de jogo) são feitos por quem chama
    e passados via DadosConquista. Isso mantém o SRP.
    """

    def construir_resultado_sucesso(
        self,
        jogador: Jogador,
        rota: Rota,
        dados: DadosConquista
    ) -> Dict:
        """
        Constrói resultado completo de sucesso.

        Args:
            jogador: Jogador que conquistou
            rota: Rota conquistada
            dados: Dados pré-calculados (pontos, trens, fim de jogo)

        Returns:
            Dict com resultado completo
        """
        # Construir mensagem
        mensagem = self._construir_mensagem_sucesso(rota, dados)

        # Montar resposta final
        return success_response(
            mensagem,
            pontos_ganhos=dados.pontos,
            cartas_descartadas=dados.cartas_descartadas,
            trens_removidos=dados.trens_removidos,
            trens_restantes=dados.trens_restantes,
            rota_dupla_bloqueada=dados.rota_dupla_bloqueada,
            fim_de_jogo_ativado=dados.fim_de_jogo_ativado,
            alerta_fim_jogo=dados.alerta_fim,
            detalhes={
                "rota_id": rota.id,
                "cidadeA": rota.cidadeA.nome,
                "cidadeB": rota.cidadeB.nome,
                "cor": rota.cor.value,
                "comprimento": rota.comprimento,
                "jogador_id": jogador.id,
                "jogador_nome": jogador.nome
            }
        )

    def construir_resultado_erro(self, mensagem: str) -> Dict:
        """
        Constrói resultado padronizado de erro.

        Args:
            mensagem: Mensagem de erro

        Returns:
            Dict com resultado de erro
        """
        return error_response(
            mensagem,
            pontos_ganhos=0,
            cartas_descartadas=0,
            trens_removidos=0,
            trens_restantes=0,
            rota_dupla_bloqueada=False,
            fim_de_jogo_ativado=False,
            alerta_fim_jogo=None,
            detalhes={}
        )

    def _construir_mensagem_sucesso(
        self,
        rota: Rota,
        dados: DadosConquista
    ) -> str:
        """Constrói mensagem de sucesso detalhada."""
        mensagem_base = (
            f"✅ Rota conquistada!\n"
            f"   📍 {rota.cidadeA.nome} → {rota.cidadeB.nome}\n"
            f"   🎯 +{dados.pontos} pontos\n"
            f"   🎴 {dados.cartas_descartadas} cartas descartadas\n"
            f"   🚂 {dados.trens_removidos} trens removidos ({dados.trens_restantes} restantes)"
        )

        if dados.fim_de_jogo_ativado and dados.alerta_fim:
            mensagem_base += f"\n\n{dados.alerta_fim}"

        return mensagem_base