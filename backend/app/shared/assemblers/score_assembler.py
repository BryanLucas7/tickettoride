"""
ScoreAssembler - Montador de pontuação final.

Padrão GRASP: Pure Fabrication
Princípio SRP: Responsável apenas por montar informações de pontuação.

Responsabilidades:
- Montar pontuação final de cada jogador
- Formatar bilhetes completos/incompletos
- Montar ranking e vencedor
"""

from typing import Dict, Any, List, Union
from ...core.domain.entities.jogo import Jogo
from ..formatters import EntityFormatters


class ScoreAssembler:
    """
    Assembler especializado para pontuação final.
    
    Single Responsibility: Monta apenas informações de pontuação
    (pontos de rotas, bilhetes, bônus, ranking).
    """
    
    @staticmethod
    def montar(
        jogo: Jogo,
        resultados: Dict[str, Any],
        vencedor: Union[str, List[str]],
        mensagem_vencedor: str
    ) -> Dict[str, Any]:
        """Alias curto para montar_pontuacao_final."""
        return ScoreAssembler.montar_pontuacao_final(
            jogo, resultados, vencedor, mensagem_vencedor
        )
    
    @staticmethod
    def montar_pontuacao_final(
        jogo: Jogo,
        resultados: Dict[str, Any],
        vencedor: Union[str, List[str]],
        mensagem_vencedor: str
    ) -> Dict[str, Any]:
        """
        Monta resposta de pontuação final do jogo.
        
        Args:
            jogo: Instância do jogo
            resultados: Dicionário com resultados de cada jogador
            vencedor: ID do vencedor ou lista de IDs em caso de empate
            mensagem_vencedor: Mensagem formatada do vencedor
            
        Returns:
            Dict formatado para resposta da API
        """
        pontuacoes = ScoreAssembler._formatar_pontuacoes(jogo, resultados)
        pontuacoes.sort(key=lambda p: p["pontuacao_total"], reverse=True)
        
        return {
            "success": True,
            "pontuacoes": pontuacoes,
            "vencedor": vencedor,
            "mensagem": mensagem_vencedor
        }
    
    @staticmethod
    def _formatar_pontuacoes(jogo: Jogo, resultados: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Formata pontuações de todos os jogadores."""
        pontuacoes = []
        
        for jogador_id, resultado in resultados.items():
            jogador = jogo.buscarJogador(jogador_id)
            pontuacoes.append(
                ScoreAssembler._formatar_pontuacao_jogador(jogador_id, jogador, resultado)
            )
        
        return pontuacoes
    
    @staticmethod
    def _formatar_pontuacao_jogador(
        jogador_id: str, 
        jogador, 
        resultado
    ) -> Dict[str, Any]:
        """Formata pontuação de um jogador específico."""
        return {
            "jogador_id": jogador_id,
            "jogador_nome": jogador.nome if jogador else f"Jogador {jogador_id}",
            "jogador_cor": jogador.cor.value if jogador else "unknown",
            "pontos_rotas": resultado.pontos_rotas,
            "bilhetes_completos": EntityFormatters.formatar_bilhetes(
                resultado.bilhetes_completos_lista,
                completos=[True] * len(resultado.bilhetes_completos_lista),
                formato="origem_destino"
            ),
            "bilhetes_incompletos": EntityFormatters.formatar_bilhetes(
                resultado.bilhetes_incompletos_lista,
                completos=[False] * len(resultado.bilhetes_incompletos_lista),
                formato="origem_destino"
            ),
            "pontos_bilhetes_positivos": resultado.pontos_bilhetes_completos,
            "pontos_bilhetes_negativos": resultado.pontos_bilhetes_incompletos,
            "bonus_maior_caminho": resultado.bonus_maior_caminho > 0,
            "pontos_maior_caminho": resultado.bonus_maior_caminho,
            "pontuacao_total": resultado.pontuacao_total,
            "tamanho_maior_caminho": resultado.comprimento_maior_caminho
        }
