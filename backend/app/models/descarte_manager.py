"""

Sistema de descarte de cartas ao conquistar rotas.

GRASP Principles Applied:
- Information Expert: DescarteManager conhece a pilha de descarte
- Controller: Gerencia o fluxo de descarte de cartas
- Low Coupling: Separado do Jogador e do Jogo

Design Decisions:
- Pilha de descarte separada do baralho principal
- Cartas descartadas podem ser reembaralhadas quando baralho acabar
"""

from dataclasses import dataclass, field
from typing import List
from .carta_vagao import CartaVagao


@dataclass
class DescarteManager:
    """
    Gerencia a pilha de descarte de cartas.
    
    GRASP Information Expert: Conhece e gerencia cartas descartadas
    """
    
    pilha_descarte: List[CartaVagao] = field(default_factory=list)
    
    def descartar_cartas(self, cartas: List[CartaVagao]) -> int:
        """Adiciona cartas à pilha de descarte
        
        Args:
            cartas: Lista de CartaVagao a serem descartadas
            
        Returns:
            Quantidade de cartas descartadas
            
        GRASP Information Expert: Gerencia a pilha de descarte
        """
        if not cartas:
            return 0
        
        self.pilha_descarte.extend(cartas)
        return len(cartas)
    
    def obter_cartas_descartadas(self) -> List[CartaVagao]:
        """Retorna todas as cartas descartadas e limpa a pilha
        
        Usado para reembaralhar quando baralho principal acabar
        
        Returns:
            Lista com todas as cartas descartadas
        """
        cartas = self.pilha_descarte[:]
        self.pilha_descarte = []
        return cartas
    
    def quantidade_descartada(self) -> int:
        """Retorna quantidade de cartas na pilha de descarte"""
        return len(self.pilha_descarte)
    
    def limpar_descarte(self):
        """Limpa a pilha de descarte (usado para reset de jogo)"""
        self.pilha_descarte = []


class ConquistaRotaService:
    """
    Serviço para processar conquista de rota completa.
    
    GRASP Controller: Coordena ações de conquista de rota
    GRASP Low Coupling: Separa lógica de descarte da UI
    
    Pure Fabrication: Classe auxiliar que não representa conceito do domínio
    """
    
    @staticmethod
    def conquistar_rota(jogador, rota, cartas_usadas: List[CartaVagao], 
                       descarte_manager: DescarteManager) -> dict:
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
