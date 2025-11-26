"""
Formatadores de entidades para padronização de responses.

Padrão GRASP: Pure Fabrication
- Centraliza responsabilidade de formatação que não pertence a nenhuma entidade específica
- Evita duplicação de código de formatação em 15+ lugares
- Facilita manutenção e padronização de formato de resposta

NOTA: Para formatação de mensagens de texto, use MessageBuilder diretamente.
"""

from typing import Dict, List, Any, Optional
from ..core.domain.entities.carta_vagao import CartaVagao
from ..core.domain.entities.bilhete_destino import BilheteDestino
from ..core.domain.entities.rota import Rota
from ..core.domain.entities.jogador import Jogador


class EntityFormatters:
    """
    Classe utilitária para formatação consistente de entidades do domínio.
    
    Responsabilidades (SRP):
    - Formatar cartas de vagão
    - Formatar bilhetes de destino
    - Formatar rotas
    - Formatar jogadores
    
    Para mensagens de texto, use MessageBuilder.
    """
    
    @staticmethod
    def formatar_carta(carta: CartaVagao) -> Dict[str, Any]:
        """
        Formata uma carta de vagão para resposta da API.
        
        Args:
            carta: CartaVagao
            
        Returns:
            Dict com cor (string) e eh_locomotiva (bool)
        """
        return {
            "cor": carta.cor.value,
            "eh_locomotiva": carta.ehLocomotiva
        }
    
    @staticmethod
    def formatar_cartas(cartas: List[CartaVagao]) -> List[Dict[str, Any]]:
        """Formata uma lista de cartas de vagão."""
        return [EntityFormatters.formatar_carta(carta) for carta in cartas]
    
    @staticmethod
    def formatar_bilhete(bilhete: BilheteDestino, completo: bool = False, formato: str = "padrao") -> Dict[str, Any]:
        """
        Formata um bilhete de destino para resposta da API.
        
        Args:
            bilhete: Instância de BilheteDestino
            completo: Se o bilhete foi completado pelo jogador
            formato: "padrao" | "compacto" | "origem_destino"
            
        Returns:
            Dict com informações do bilhete formatadas
        """
        if formato == "compacto":
            return {
                "origem": bilhete.cidadeOrigem.nome,
                "destino": bilhete.cidadeDestino.nome,
                "pontos": bilhete.pontos
            }
        elif formato == "origem_destino":
            return {
                "origem": bilhete.cidadeOrigem.nome,
                "destino": bilhete.cidadeDestino.nome,
                "pontos": bilhete.pontos,
                "completo": completo
            }
        else:  # formato "padrao"
            resultado = {
                "id": bilhete.id,
                "cidadeOrigem": bilhete.cidadeOrigem.nome,
                "cidadeDestino": bilhete.cidadeDestino.nome,
                "pontos": bilhete.pontos
            }
            if completo is not None:
                resultado["completo"] = completo
            return resultado
    
    @staticmethod
    def formatar_bilhetes(bilhetes: List[BilheteDestino], completos: Optional[List[bool]] = None, formato: str = "padrao") -> List[Dict[str, Any]]:
        """Formata uma lista de bilhetes de destino."""
        if completos is None:
            completos = [False] * len(bilhetes)
        
        return [
            EntityFormatters.formatar_bilhete(bilhete, completo, formato)
            for bilhete, completo in zip(bilhetes, completos)
        ]
    
    @staticmethod
    def formatar_rota(rota: Rota) -> Dict[str, Any]:
        """Formata uma rota para resposta da API."""
        return {
            "id": rota.id,
            "origem": rota.cidadeA.nome,
            "destino": rota.cidadeB.nome,
            "cor": rota.cor.value if rota.cor else None,
            "tamanho": rota.comprimento,
            "proprietario": rota.proprietario.id if rota.proprietario else None,
            "conquistada": rota.proprietario is not None
        }
    
    @staticmethod
    def formatar_rotas(rotas: List[Rota]) -> List[Dict[str, Any]]:
        """Formata uma lista de rotas."""
        return [EntityFormatters.formatar_rota(rota) for rota in rotas]
    
    @staticmethod
    def formatar_jogador(jogador: Jogador, incluir_cartas: bool = False, incluir_bilhetes: bool = False) -> Dict[str, Any]:
        """Formata informações de um jogador para resposta da API."""
        resultado = {
            "id": jogador.id,
            "nome": jogador.nome,
            "cor": jogador.cor.value,
            "pontos": jogador.pontuacao,
            "trens_restantes": len(jogador.vagoes),
            "num_cartas": len(jogador.cartasVagao),
            "num_bilhetes": len(jogador.bilhetes)
        }
        
        if incluir_cartas:
            resultado["cartas"] = EntityFormatters.formatar_cartas(jogador.cartasVagao)
        
        if incluir_bilhetes:
            resultado["bilhetes"] = EntityFormatters.formatar_bilhetes(jogador.bilhetes)
        
        return resultado
    
    @staticmethod
    def formatar_jogadores(jogadores: List[Jogador], incluir_cartas: bool = False, incluir_bilhetes: bool = False) -> List[Dict[str, Any]]:
        """Formata uma lista de jogadores."""
        return [
            EntityFormatters.formatar_jogador(jogador, incluir_cartas, incluir_bilhetes)
            for jogador in jogadores
        ]
