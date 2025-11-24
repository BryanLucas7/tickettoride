"""
Service para ações comuns do jogo (passar turno, verificar fim, etc.)

GRASP: 
- Pure Fabrication: Serviço criado para evitar duplicação de lógica
- Low Coupling: Centraliza lógica de fim de jogo
- High Cohesion: Responsável apenas por ações de turno/fim de jogo
"""

from typing import Dict, Any
from ...core.domain.entities.jogo import Jogo


class GameActionService:
    """
    Serviço responsável por ações comuns do jogo.
    
    Centraliza lógica de:
    - Passar turno
    - Verificar e processar fim de jogo
    - Resetar estado de compra de cartas
    """
    
    def passar_turno_e_verificar_fim(self, jogo: Jogo) -> Dict[str, Any]:
        """
        Passa o turno e verifica se o jogo terminou (última rodada).
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            Dicionário com:
            - jogo_terminou: bool - Se o jogo terminou
            - mensagem_fim: str|None - Mensagem de fim (se terminou)
            - proximo_jogador: str - ID do próximo jogador
        """
        # Reseta estado de compra de cartas para o próximo turno
        jogo.resetar_estado_compra()
        
        # Avança para o próximo turno
        jogo.passar_turno()
        
        # Verifica se está na última rodada e processa
        jogo_terminou = False
        mensagem_fim = None
        
        if jogo.gerenciadorFimDeJogo and jogo.gerenciadorFimDeJogo.ultima_rodada_ativada:
            resultado_fim = jogo.gerenciadorFimDeJogo.processar_turno_jogado()
            
            if resultado_fim["jogo_terminou"]:
                jogo.encerrar()
                jogo_terminou = True
                mensagem_fim = resultado_fim["mensagem"]
        
        return {
            "jogo_terminou": jogo_terminou,
            "mensagem_fim": mensagem_fim,
            "proximo_jogador": jogo.gerenciadorDeTurnos.jogadorAtual
        }
    
    def formatar_resposta_com_fim_turno(
        self, 
        jogo: Jogo, 
        response_base: Dict[str, Any], 
        passar_turno: bool = True
    ) -> Dict[str, Any]:
        """
        Formata resposta de uma ação do jogo com informações de fim de turno.
        
        Este método centraliza a lógica de adicionar informações de turno
        e fim de jogo às respostas, evitando duplicação em múltiplos services.
        
        Args:
            jogo: Instância do jogo
            response_base: Dicionário base com a resposta da ação
            passar_turno: Se True, passa o turno automaticamente
            
        Returns:
            Dicionário response_base atualizado com:
            - turn_completed: bool - Se o turno foi completado
            - turno_passado: bool - Se o turno foi passado
            - next_player: str|None - ID do próximo jogador (se turno passado)
            - jogo_terminou: bool|None - Se o jogo terminou (se turno passado)
            - mensagem_fim: str|None - Mensagem de fim (se jogo terminou)
            
        Example:
            >>> response = {"success": True, "message": "Carta comprada"}
            >>> service.formatar_resposta_com_fim_turno(jogo, response)
            {
                "success": True,
                "message": "Carta comprada",
                "turn_completed": True,
                "turno_passado": True,
                "next_player": "player_2",
                "jogo_terminou": False,
                "mensagem_fim": None
            }
        """
        turno_completo = jogo.estadoCompraCartas.turnoCompleto if hasattr(jogo, 'estadoCompraCartas') else passar_turno
        
        response_base["turn_completed"] = turno_completo
        
        if passar_turno and turno_completo:
            resultado_turno = self.passar_turno_e_verificar_fim(jogo)
            response_base.update({
                "turno_passado": True,
                "next_player": resultado_turno["proximo_jogador"],
                "jogo_terminou": resultado_turno["jogo_terminou"],
                "mensagem_fim": resultado_turno["mensagem_fim"]
            })
        else:
            response_base["turno_passado"] = False
        
        return response_base
