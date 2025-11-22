"""

Serviço para processar conquista de rota completa.

GRASP Controller: Coordena ações de conquista de rota
GRASP Low Coupling: Separa lógica de descarte da UI

Pure Fabrication: Classe auxiliar que não representa conceito do domínio
"""

from typing import List, TYPE_CHECKING
from ..entities.carta_vagao import CartaVagao

if TYPE_CHECKING:
    from .descarte_manager import DescarteManager


class ConquistaRotaService:
    """
    Serviço para processar conquista de rota completa.
    
    GRASP Controller: Coordena ações de conquista de rota
    GRASP Low Coupling: Separa lógica de descarte da UI
    
    Pure Fabrication: Classe auxiliar que não representa conceito do domínio
    """
    
    @staticmethod
    def conquistar_rota(jogador, rota, cartas_usadas: List[CartaVagao], 
                       descarte_manager: 'DescarteManager') -> dict:
        """Processa conquista completa de rota
        
        Args:
            jogador: Jogador que está conquistando
            rota: Rota sendo conquistada
            cartas_usadas: Lista de cartas que o jogador usará
            descarte_manager: Gerenciador de descarte
            
        Returns:
            dict com resultado da operação: {
                "sucesso": bool,
                "mensagem": str,
                "cartas_descartadas": int,
                "trens_removidos": int,
                "trens_restantes": int
            }
            
        GRASP Controller: Coordena validação, descarte e remoção de trens
        """
        
        # 1. Valida se jogador tem trens suficientes
        trens_necessarios = rota.comprimento
        if len(jogador.vagoes) < trens_necessarios:
            return {
                "sucesso": False,
                "mensagem": f"Trens insuficientes: tem {len(jogador.vagoes)}, precisa de {trens_necessarios}",
                "cartas_descartadas": 0,
                "trens_removidos": 0,
                "trens_restantes": len(jogador.vagoes)
            }
        
        # 2. Valida se jogador tem as cartas usadas
        for carta in cartas_usadas:
            if carta not in jogador.mao.cartasVagao:
                return {
                    "sucesso": False,
                    "mensagem": f"Carta não encontrada na mão do jogador",
                    "cartas_descartadas": 0,
                    "trens_removidos": 0,
                    "trens_restantes": len(jogador.vagoes)
                }
        
        # 3. Remove cartas da mão do jogador para evitar duplicidade entre mão e descarte
        sucesso_remocao = jogador.removerCartasVagao(cartas_usadas)
        if not sucesso_remocao:
            return {
                "sucesso": False,
                "mensagem": "Falha ao remover cartas da mão",
                "cartas_descartadas": 0,
                "trens_removidos": 0,
                "trens_restantes": len(jogador.vagoes)
            }
        
        # 4. Descarta cartas usadas
        qtd_descartada = descarte_manager.descartar_cartas(cartas_usadas)
        
        # 5. Remove trens do jogador
        trens_removidos = 0
        for _ in range(trens_necessarios):
            if jogador.vagoes:
                jogador.vagoes.pop()
                trens_removidos += 1
        
        return {
            "sucesso": True,
            "mensagem": f"Rota conquistada! Descartadas {qtd_descartada} cartas, removidos {trens_removidos} trens",
            "cartas_descartadas": qtd_descartada,
            "trens_removidos": trens_removidos,
            "trens_restantes": len(jogador.vagoes)
        }