"""

Implementa detecção automática de fim de jogo.

Regra: Quando um jogador chega a ≤2 trens, todos os jogadores jogam mais 1 último turno.

GRASP Principles:
- Controller: Gerenciador controla fluxo de fim de jogo
- Information Expert: Gerenciador conhece estado dos turnos
- Protected Variations: Encapsula lógica de fim de jogo
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class GerenciadorFimDeJogo:
    """
    Gerencia detecção e controle de fim de jogo.
    
    GRASP Controller: Controla fluxo de detecção e última rodada
    GRASP Information Expert: Conhece estado de fim de jogo e turnos restantes
    """
    
    ultima_rodada_ativada: bool = False
    jogador_que_ativou_fim: Optional[str] = None
    turnos_restantes: int = 0
    total_jogadores: int = 0
    
    def verificar_condicao_fim(self, jogador_id: str, trens_restantes: int) -> dict:
        """Verifica se jogador atingiu condição de fim de jogo (≤2 trens)
        
        Args:
            jogador_id: ID do jogador
            trens_restantes: Quantidade de trens restantes
            
        Returns:
            dict com resultado: {
                "fim_ativado": bool,
                "ultima_rodada": bool,
                "turnos_restantes": int,
                "mensagem": str
            }
        """
        
        # Se já está em última rodada, não faz nada
        if self.ultima_rodada_ativada:
            return {
                "fim_ativado": False,
                "ultima_rodada": True,
                "turnos_restantes": self.turnos_restantes,
                "mensagem": f"Última rodada já ativada. Restam {self.turnos_restantes} turnos"
            }
        
        # Verifica condição: ≤2 trens
        if trens_restantes <= 2:
            self.ativar_ultima_rodada(jogador_id)
            
            return {
                "fim_ativado": True,
                "ultima_rodada": True,
                "turnos_restantes": self.turnos_restantes,
                "mensagem": f"🚨 {jogador_id} chegou a {trens_restantes} trens! Última rodada iniciada: {self.turnos_restantes} turnos restantes"
            }
        
        return {
            "fim_ativado": False,
            "ultima_rodada": False,
            "turnos_restantes": 0,
            "mensagem": f"Jogo continua. {jogador_id} tem {trens_restantes} trens"
        }
    
    def ativar_ultima_rodada(self, jogador_id: str):
        """Ativa última rodada do jogo
        
        Args:
            jogador_id: ID do jogador que ativou fim
        """
        self.ultima_rodada_ativada = True
        self.jogador_que_ativou_fim = jogador_id
        # Cada jogador joga mais 1 turno
        self.turnos_restantes = self.total_jogadores
    
    def processar_turno_jogado(self) -> dict:
        """Processa fim de turno na última rodada
        
        Decrementa contador de turnos e verifica se jogo terminou.
        
        Returns:
            dict com resultado: {
                "jogo_terminou": bool,
                "turnos_restantes": int,
                "mensagem": str
            }
        """
        
        if not self.ultima_rodada_ativada:
            return {
                "jogo_terminou": False,
                "turnos_restantes": 0,
                "mensagem": "Jogo ainda não está em última rodada"
            }
        
        # Decrementa turno
        self.turnos_restantes -= 1
        
        # Verifica se terminou
        if self.turnos_restantes <= 0:
            return {
                "jogo_terminou": True,
                "turnos_restantes": 0,
                "mensagem": "🎮 Jogo terminou! Calculando pontuação final..."
            }
        
        return {
            "jogo_terminou": False,
            "turnos_restantes": self.turnos_restantes,
            "mensagem": f"Última rodada: {self.turnos_restantes} turnos restantes"
        }
    
    def obter_estado(self) -> dict:
        """Retorna estado atual do gerenciador
        
        Returns:
            dict com estado completo
        """
        return {
            "ultima_rodada": self.ultima_rodada_ativada,
            "jogador_que_ativou": self.jogador_que_ativou_fim,
            "turnos_restantes": self.turnos_restantes,
            "total_jogadores": self.total_jogadores
        }
    
    def resetar(self):
        """Reseta gerenciador para novo jogo"""
        self.ultima_rodada_ativada = False
        self.jogador_que_ativou_fim = None
        self.turnos_restantes = 0
