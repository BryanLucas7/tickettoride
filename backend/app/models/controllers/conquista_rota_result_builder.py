"""
Construtor de resultados para conquista de rotas.

PADRÃO GRASP: Pure Fabrication
- ConquistaRotaResultBuilder constrói respostas padronizadas
- Separa lógica de formatação do controller

Responsabilidades:
- Calcular pontos ganhos
- Adicionar pontos ao placar
- Verificar condições de fim de jogo
- Construir mensagens de sucesso
- Montar resposta final
"""

from typing import Dict, Optional
from ..entities.jogador import Jogador
from ..entities.rota import Rota
from ..calculators.calculadora_pontos_rota import CalculadoraPontosRota
from ..calculators.placar import Placar
from ..managers.gerenciador_fim_jogo import GerenciadorFimDeJogo


class ConquistaRotaResultBuilder:
    """
    Pure Fabrication - Constrói resultados padronizados para conquista de rotas.

    Responsabilidades:
    - Calcular pontos ganhos
    - Adicionar pontos ao placar
    - Verificar condições de fim de jogo
    - Construir mensagens de sucesso
    - Montar resposta final

    GRASP Principles:
    - Pure Fabrication: Classe criada para responsabilidade específica
    - Information Expert: Conhece formato das respostas
    - Low Coupling: Recebe dependências por parâmetro
    - High Cohesion: Focado apenas em construção de resultados
    """

    def __init__(
        self,
        placar: Optional[Placar] = None,
        gerenciador_fim_jogo: Optional[GerenciadorFimDeJogo] = None
    ):
        """
        Inicializa o construtor.

        Args:
            placar: Placar do jogo (opcional)
            gerenciador_fim_jogo: Gerenciador de fim de jogo (opcional)
        """
        self.placar = placar
        self.gerenciador_fim_jogo = gerenciador_fim_jogo

    def construir_resultado_sucesso(
        self,
        jogador: Jogador,
        rota: Rota,
        resultado_conquista: Dict,
        rota_dupla_bloqueada: bool
    ) -> Dict:
        """
        Constrói resultado completo de sucesso.

        Args:
            jogador: Jogador que conquistou
            rota: Rota conquistada
            resultado_conquista: Resultado do processamento físico
            rota_dupla_bloqueada: Se rota dupla foi bloqueada

        Returns:
            Dict com resultado completo
        """
        # 1. Calcular pontos
        pontos = CalculadoraPontosRota.calcular_pontos(rota.comprimento)

        # 2. Adicionar pontos ao jogador (Observer Pattern)
        if self.placar:
            self.placar.adicionar_pontos_rota(
                jogador_id=jogador.id,
                comprimento_rota=rota.comprimento,
                nome_rota=f"{rota.cidadeA.nome} → {rota.cidadeB.nome}"
            )

        # 3. Verificar fim de jogo
        fim_de_jogo_ativado = False
        alerta_fim = None

        if self.gerenciador_fim_jogo:
            trens_restantes = resultado_conquista["trens_restantes"]
            estado_fim = self.gerenciador_fim_jogo.verificar_condicao_fim(
                jogador_id=jogador.id,
                trens_restantes=trens_restantes
            )

            fim_de_jogo_ativado = estado_fim.get("fim_ativado", False)
            alerta_fim = estado_fim.get("mensagem")

        # 4. Construir mensagem
        mensagem = self._construir_mensagem_sucesso(
            rota=rota,
            pontos=pontos,
            cartas_descartadas=resultado_conquista["cartas_descartadas"],
            trens_removidos=resultado_conquista["trens_removidos"],
            trens_restantes=resultado_conquista["trens_restantes"],
            fim_de_jogo_ativado=fim_de_jogo_ativado,
            alerta_fim=alerta_fim
        )

        # 5. Montar resposta final
        return {
            "sucesso": True,
            "mensagem": mensagem,
            "pontos_ganhos": pontos,
            "cartas_descartadas": resultado_conquista["cartas_descartadas"],
            "trens_removidos": resultado_conquista["trens_removidos"],
            "trens_restantes": resultado_conquista["trens_restantes"],
            "rota_dupla_bloqueada": rota_dupla_bloqueada,
            "fim_de_jogo_ativado": fim_de_jogo_ativado,
            "alerta_fim_jogo": alerta_fim,
            "detalhes": {
                "rota_id": rota.id,
                "cidadeA": rota.cidadeA.nome,
                "cidadeB": rota.cidadeB.nome,
                "cor": rota.cor.value,
                "comprimento": rota.comprimento,
                "jogador_id": jogador.id,
                "jogador_nome": jogador.nome
            }
        }

    def construir_resultado_erro(self, mensagem: str) -> Dict:
        """
        Constrói resultado padronizado de erro.

        Args:
            mensagem: Mensagem de erro

        Returns:
            Dict com resultado de erro
        """
        return {
            "sucesso": False,
            "mensagem": mensagem,
            "pontos_ganhos": 0,
            "cartas_descartadas": 0,
            "trens_removidos": 0,
            "trens_restantes": 0,
            "rota_dupla_bloqueada": False,
            "fim_de_jogo_ativado": False,
            "alerta_fim_jogo": None,
            "detalhes": {}
        }

    def _construir_mensagem_sucesso(
        self,
        rota: Rota,
        pontos: int,
        cartas_descartadas: int,
        trens_removidos: int,
        trens_restantes: int,
        fim_de_jogo_ativado: bool,
        alerta_fim: Optional[str]
    ) -> str:
        """Constrói mensagem de sucesso detalhada"""
        mensagem_base = (
            f"✅ Rota conquistada!\n"
            f"   📍 {rota.cidadeA.nome} → {rota.cidadeB.nome}\n"
            f"   🎯 +{pontos} pontos\n"
            f"   🎴 {cartas_descartadas} cartas descartadas\n"
            f"   🚂 {trens_removidos} trens removidos ({trens_restantes} restantes)"
        )

        if fim_de_jogo_ativado and alerta_fim:
            mensagem_base += f"\n\n{alerta_fim}"

        return mensagem_base