"""
MessageBuilder - Construtor de mensagens de negócio.

Padrão GRASP: Pure Fabrication
- Extraído de formatters.py para separar responsabilidades
- Formatters: conversão entidade → dict (JSON)
- MessageBuilder: criação de mensagens legíveis para humanos

Responsabilidades:
- Criar mensagens de compra de bilhetes
- Criar mensagens de conquista de rotas
- Criar mensagens de fim de jogo
- Criar mensagens de turno
"""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.domain.entities.bilhete_destino import BilheteDestino


class MessageBuilder:
    """
    Construtor de mensagens de negócio para respostas da API.
    
    Separa a responsabilidade de criar mensagens legíveis da
    responsabilidade de formatar entidades para JSON.
    """
    
    @staticmethod
    def formatar_rotas_bilhetes(bilhetes: List['BilheteDestino']) -> str:
        """
        Formata lista de bilhetes como texto de rotas compacto.
        
        Args:
            bilhetes: Lista de bilhetes
            
        Returns:
            String formatada: "São Paulo → Rio, Brasília → Salvador"
            Retorna string vazia se lista vazia
            
        Example:
            >>> bilhetes = [bilhete1, bilhete2]
            >>> MessageBuilder.formatar_rotas_bilhetes(bilhetes)
            'São Paulo → Rio de Janeiro, Curitiba → Porto Alegre'
        """
        if not bilhetes:
            return ""
        
        return ", ".join(
            f"{b.cidadeOrigem.nome} → {b.cidadeDestino.nome}"
            for b in bilhetes
        )
    
    @staticmethod
    def criar_mensagem_compra_bilhetes(
        jogador_nome: str,
        bilhetes_escolhidos: List['BilheteDestino'],
        quantidade_recusados: int
    ) -> str:
        """
        Cria mensagem formatada de compra de bilhetes.
        
        Args:
            jogador_nome: Nome do jogador
            bilhetes_escolhidos: Bilhetes que o jogador ficou
            quantidade_recusados: Quantidade devolvida
            
        Returns:
            Mensagem formatada e legível
            
        Example:
            >>> MessageBuilder.criar_mensagem_compra_bilhetes(
            ...     "João", [bilhete1, bilhete2], 1
            ... )
            'João ficou com 2 bilhete(s) e devolveu 1. Bilhetes escolhidos: SP → RJ, BH → PE.'
        """
        quantidade_escolhidos = len(bilhetes_escolhidos)
        mensagem = (
            f"{jogador_nome} ficou com {quantidade_escolhidos} bilhete(s)"
            f" e devolveu {quantidade_recusados}."
        )
        
        if bilhetes_escolhidos:
            rotas = MessageBuilder.formatar_rotas_bilhetes(bilhetes_escolhidos)
            mensagem += f" Bilhetes escolhidos: {rotas}."
        
        return mensagem
    
    @staticmethod
    def criar_mensagem_conquista_rota(
        cidade_origem: str,
        cidade_destino: str,
        pontos: int,
        cartas_descartadas: int,
        trens_removidos: int,
        trens_restantes: int
    ) -> str:
        """
        Cria mensagem formatada de conquista de rota.
        
        Args:
            cidade_origem: Nome da cidade de origem
            cidade_destino: Nome da cidade de destino
            pontos: Pontos ganhos
            cartas_descartadas: Número de cartas descartadas
            trens_removidos: Número de trens removidos
            trens_restantes: Número de trens restantes
            
        Returns:
            Mensagem formatada e legível
        """
        return (
            f"✅ Rota conquistada!\n"
            f"   📍 {cidade_origem} → {cidade_destino}\n"
            f"   🎯 +{pontos} pontos\n"
            f"   🎴 {cartas_descartadas} cartas descartadas\n"
            f"   🚂 {trens_removidos} trens removidos ({trens_restantes} restantes)"
        )
    
    @staticmethod
    def criar_mensagem_vencedor(nomes_vencedores: List[str]) -> str:
        """
        Cria mensagem de vencedor.
        
        Args:
            nomes_vencedores: Lista com nome(s) do(s) vencedor(es)
            
        Returns:
            Mensagem formatada
        """
        if len(nomes_vencedores) > 1:
            return f"Empate! Vencedores: {', '.join(nomes_vencedores)}"
        return f"{nomes_vencedores[0]} venceu o jogo!"
    
    @staticmethod
    def criar_mensagem_turno_passado(proximo_jogador: str) -> str:
        """
        Cria mensagem de turno passado.
        
        Args:
            proximo_jogador: ID ou nome do próximo jogador
            
        Returns:
            Mensagem formatada
        """
        return f"Turno passado para jogador {proximo_jogador}"
