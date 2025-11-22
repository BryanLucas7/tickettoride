"""
Geração de alertas para frontend sobre fim de jogo.

GRASP Information Expert: Conhece mensagens de alerta
GRASP Low Coupling: Separado da lógica de detecção
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class AlertaFimDeJogo:
    """
    Gera alertas para frontend sobre fim de jogo.

    GRASP Information Expert: Conhece mensagens de alerta
    GRASP Low Coupling: Separado da lógica de detecção
    """

    alertas: List[dict] = field(default_factory=list)

    def criar_alerta_ultima_rodada(self, jogador_id: str, trens: int, turnos: int) -> dict:
        """Cria alerta de última rodada

        Args:
            jogador_id: Jogador que ativou
            trens: Quantidade de trens restantes
            turnos: Turnos restantes

        Returns:
            dict com alerta formatado
        """
        alerta = {
            "tipo": "ULTIMA_RODADA",
            "nivel": "CRITICO",
            "titulo": "🚨 ÚLTIMA RODADA!",
            "mensagem": f"{jogador_id} chegou a {trens} trens!",
            "detalhes": f"Todos os jogadores jogam mais {turnos} turno(s)",
            "icone": "⏰",
            "cor": "vermelho"
        }

        self.alertas.append(alerta)
        return alerta

    def criar_alerta_turno_restante(self, turnos: int) -> dict:
        """Cria alerta de turnos restantes

        Args:
            turnos: Quantidade de turnos restantes

        Returns:
            dict com alerta formatado
        """
        alerta = {
            "tipo": "TURNO_RESTANTE",
            "nivel": "AVISO",
            "titulo": f"⏰ {turnos} turno(s) restante(s)",
            "mensagem": f"O jogo está terminando",
            "detalhes": "Última rodada em andamento",
            "icone": "⚠️",
            "cor": "amarelo"
        }

        self.alertas.append(alerta)
        return alerta

    def criar_alerta_jogo_terminou(self) -> dict:
        """Cria alerta de jogo terminado

        Returns:
            dict com alerta formatado
        """
        alerta = {
            "tipo": "JOGO_TERMINOU",
            "nivel": "INFO",
            "titulo": "🎮 Jogo Terminado!",
            "mensagem": "Calculando pontuação final...",
            "detalhes": "Prepare-se para os resultados",
            "icone": "🏆",
            "cor": "verde"
        }

        self.alertas.append(alerta)
        return alerta

    def obter_alertas(self) -> List[dict]:
        """Retorna todos os alertas"""
        return self.alertas

    def limpar_alertas(self):
        """Limpa todos os alertas"""
        self.alertas.clear()