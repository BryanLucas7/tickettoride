"""
GameStateAssembler - Montador de estado do jogo.

Padrão GRASP: Pure Fabrication
Princípio SRP: Responsável apenas por montar estado geral do jogo.

Responsabilidades:
- Montar estado completo do jogo
- Formatar jogadores com informações básicas
- Formatar cartas visíveis na mesa
"""

from typing import Dict, Any, Optional
from ...core.domain.entities.jogo import Jogo
from ..formatters import EntityFormatters


class GameStateAssembler:
    """
    Assembler especializado para estado do jogo.
    
    Single Responsibility: Monta apenas informações gerais do jogo
    (jogadores, cartas visíveis, status).
    """
    
    @staticmethod
    def montar_estado_completo(jogo: Jogo, jogador_atual_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Monta estado completo do jogo para resposta da API.
        
        Agrega: jogadores, cartas visíveis, status do jogo.
        
        Args:
            jogo: Instância do jogo
            jogador_atual_id: ID do jogador atual (opcional, usa gerenciador se None)
            
        Returns:
            Dict com estado completo do jogo
            
        Example:
            >>> estado = GameStateAssembler.montar_estado_completo(jogo)
            >>> estado.keys()
            dict_keys(['game_id', 'iniciado', 'finalizado', 'jogadores', ...])
        """
        jogador_atual_id = GameStateAssembler._determinar_jogador_atual(jogo, jogador_atual_id)
        jogadores_formatados = GameStateAssembler._formatar_jogadores(jogo)
        cartas_visiveis, cartas_fechadas = GameStateAssembler._formatar_cartas_mesa(jogo)
        
        return {
            "game_id": jogo.id,
            "iniciado": jogo.estado.iniciado,
            "finalizado": jogo.estado.finalizado,
            "jogadores": jogadores_formatados,
            "jogador_atual_id": jogador_atual_id,
            "cartas_visiveis": cartas_visiveis,
            "cartas_fechadas_restantes": cartas_fechadas,
            "cartas_fechadas_disponiveis": cartas_fechadas,
            "pode_comprar_carta_fechada": cartas_fechadas > 0,
            "bilhetes_restantes": GameStateAssembler._bilhetes_restantes(jogo)
        }
    
    @staticmethod
    def _determinar_jogador_atual(jogo: Jogo, jogador_atual_id: Optional[str]) -> Optional[str]:
        """Determina o ID do jogador atual."""
        if jogador_atual_id is None and jogo.estado.iniciado:
            jogador_atual = jogo.gerenciadorDeTurnos.getJogadorAtual()
            return jogador_atual.id if jogador_atual else None
        return jogador_atual_id
    
    @staticmethod
    def _formatar_jogadores(jogo: Jogo) -> list:
        """Formata lista de jogadores com informações básicas."""
        jogadores_formatados = []
        for jogador in jogo.gerenciadorDeTurnos.jogadores:
            jogador_info = EntityFormatters.formatar_jogador(
                jogador, 
                incluir_cartas=False, 
                incluir_bilhetes=False
            )
            if jogo.estado.placar:
                jogador_info["pontos"] = jogo.estado.placar.obter_pontuacao(jogador.id)
            jogadores_formatados.append(jogador_info)
        return jogadores_formatados
    
    @staticmethod
    def _formatar_cartas_mesa(jogo: Jogo) -> tuple:
        """Formata cartas visíveis e conta cartas fechadas."""
        cartas_visiveis = []
        cartas_fechadas_restantes = 0
        
        if jogo.gerenciadorDeBaralhoVagoes:
            cartas_visiveis = EntityFormatters.formatar_cartas(
                jogo.gerenciadorDeBaralhoVagoes.cartasAbertas
            )
            cartas_fechadas_restantes = len(jogo.gerenciadorDeBaralhoVagoes.baralhoVagoes.cartas)
        
        return cartas_visiveis, cartas_fechadas_restantes

    @staticmethod
    def _bilhetes_restantes(jogo: Jogo) -> int:
        """Retorna quantidade de bilhetes de destino restantes no baralho."""
        if jogo.gerenciadorDeBaralhoBilhetes:
            return jogo.gerenciadorDeBaralhoBilhetes.quantidade_restante
        return 0
