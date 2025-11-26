"""
PlayerHandAssembler - Montador de mão do jogador.

Padrão GRASP: Pure Fabrication
Princípio SRP: Responsável apenas por montar informações da mão do jogador.

Responsabilidades:
- Montar cartas na mão do jogador
- Montar bilhetes com status de completude
- Formatar estatísticas do jogador
"""

from typing import Dict, Any, List
from ...core.domain.entities.jogo import Jogo
from ...core.domain.entities.jogador import Jogador
from ..formatters import EntityFormatters


class PlayerHandAssembler:
    """
    Assembler especializado para mão do jogador.
    
    Single Responsibility: Monta apenas informações da mão
    (cartas, bilhetes, estatísticas pessoais).
    """
    
    @staticmethod
    def montar_mao_completa(
        jogo: Jogo, 
        jogador: Jogador, 
        incluir_bilhetes: bool = True,
        incluir_cartas: bool = True,
        verificar_bilhetes_completos: bool = True
    ) -> Dict[str, Any]:
        """
        Monta informações completas da mão de um jogador.
        
        Args:
            jogo: Instância do jogo
            jogador: Instância do jogador
            incluir_bilhetes: Se deve incluir bilhetes
            incluir_cartas: Se deve incluir cartas
            verificar_bilhetes_completos: Se deve verificar bilhetes completos
            
        Returns:
            Dict com cartas, bilhetes e estatísticas do jogador
        """
        resposta = PlayerHandAssembler._montar_info_basica(jogo, jogador)
        
        if incluir_cartas:
            resposta["cartas"] = EntityFormatters.formatar_cartas(jogador.cartasVagao)
        
        if incluir_bilhetes:
            resposta["bilhetes"] = PlayerHandAssembler._formatar_bilhetes(
                jogo, jogador, verificar_bilhetes_completos
            )
        
        return resposta
    
    @staticmethod
    def _montar_info_basica(jogo: Jogo, jogador: Jogador) -> Dict[str, Any]:
        """Monta informações básicas do jogador."""
        return {
            "player_id": jogador.id,
            "nome": jogador.nome,
            "cor": jogador.cor.value,
            "num_cartas": len(jogador.cartasVagao),
            "num_bilhetes": len(jogador.bilhetes),
            "trens_restantes": len(jogador.vagoes),
            "pontos": jogo.estado.placar.obter_pontuacao(jogador.id) if jogo.estado.placar else 0
        }
    
    @staticmethod
    def _formatar_bilhetes(
        jogo: Jogo, 
        jogador: Jogador, 
        verificar_completos: bool
    ) -> List[Dict[str, Any]]:
        """Formata bilhetes com ou sem verificação de completude."""
        if verificar_completos and jogo.pathfinder:
            rotas_jogador = jogo.rotas_do_jogador(jogador)
            completos_status = [
                jogo.pathfinder.verificar_bilhete_completo(
                    bilhete=bilhete,
                    rotas_conquistadas=rotas_jogador
                )
                for bilhete in jogador.bilhetes
            ]
            return EntityFormatters.formatar_bilhetes(
                jogador.bilhetes, 
                completos=completos_status
            )
        
        return EntityFormatters.formatar_bilhetes(jogador.bilhetes)
