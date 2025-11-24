"""
Formatadores de entidades para padronização de responses.

Padrão GRASP: Pure Fabrication
- Centraliza responsabilidade de formatação que não pertence a nenhuma entidade específica
- Evita duplicação de código de formatação em 15+ lugares
- Facilita manutenção e padronização de formato de resposta
"""

from typing import Dict, List, Any, Optional
from ..core.domain.entities.carta_vagao import CartaVagao
from ..core.domain.entities.bilhete_destino import BilheteDestino
from ..core.domain.entities.rota import Rota
from ..core.domain.entities.jogador import Jogador


class EntityFormatters:
    """
    Classe utilitária para formatação consistente de entidades do domínio.
    
    Todos os métodos são estáticos pois não mantêm estado e servem
    apenas como funções de transformação.
    """
    
    @staticmethod
    def formatar_carta(carta: CartaVagao) -> Dict[str, Any]:
        """
        Formata uma carta de vagão para resposta da API.
        
        Args:
            carta: CartaVagao
            
        Returns:
            Dict com cor (string) e eh_locomotiva (bool)
            
        Example:
            >>> carta = CartaVagao(cor=Cor.VERMELHO, ehLocomotiva=False)
            >>> EntityFormatters.formatar_carta(carta)
            {'cor': 'vermelho', 'eh_locomotiva': False}
        """
        return {
            "cor": carta.cor.value,
            "eh_locomotiva": carta.ehLocomotiva
        }
    
    @staticmethod
    def formatar_cartas(cartas: List[CartaVagao]) -> List[Dict[str, Any]]:
        """
        Formata uma lista de cartas de vagão.
        
        Args:
            cartas: Lista de CartaVagao
            
        Returns:
            Lista de dicts formatados
            
        Example:
            >>> cartas = [CartaVagao(cor=Cor.AZUL), CartaVagao(cor=Cor.VERDE)]
            >>> EntityFormatters.formatar_cartas(cartas)
            [{'cor': 'azul', 'eh_locomotiva': False}, {'cor': 'verde', 'eh_locomotiva': False}]
        """
        return [EntityFormatters.formatar_carta(carta) for carta in cartas]
    
    @staticmethod
    def formatar_bilhete(bilhete: BilheteDestino, completo: bool = False, formato: str = "padrao") -> Dict[str, Any]:
        """
        Formata um bilhete de destino para resposta da API.
        
        Args:
            bilhete: Instância de BilheteDestino
            completo: Se o bilhete foi completado pelo jogador
            formato: Tipo de formatação ("padrao", "compacto", "origem_destino")
                - "padrao": cidadeOrigem, cidadeDestino, pontos, completo
                - "compacto": origem, destino, pontos
                - "origem_destino": origem, destino, pontos, completo
            
        Returns:
            Dict com informações do bilhete formatadas
            
        Example:
            >>> bilhete = BilheteDestino(cidadeOrigem=cidade1, cidadeDestino=cidade2, pontos=10)
            >>> EntityFormatters.formatar_bilhete(bilhete, completo=True)
            {'id': '...', 'cidadeOrigem': 'São Paulo', 'cidadeDestino': 'Rio', 'pontos': 10, 'completo': True}
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
        """
        Formata uma lista de bilhetes de destino.
        
        Args:
            bilhetes: Lista de BilheteDestino
            completos: Lista opcional de status de completude (mesma ordem que bilhetes)
            formato: Tipo de formatação a usar
            
        Returns:
            Lista de dicts formatados
        """
        if completos is None:
            completos = [False] * len(bilhetes)
        
        return [
            EntityFormatters.formatar_bilhete(bilhete, completo, formato)
            for bilhete, completo in zip(bilhetes, completos)
        ]
    
    @staticmethod
    def formatar_rota(rota: Rota) -> Dict[str, Any]:
        """
        Formata uma rota para resposta da API.
        
        Args:
            rota: Instância de Rota
            
        Returns:
            Dict com informações da rota
            
        Example:
            >>> rota = Rota(id="SP-RJ", cidadeOrigem=sp, cidadeDestino=rj, cor=Cor.AZUL, tamanho=3)
            >>> EntityFormatters.formatar_rota(rota)
            {'id': 'SP-RJ', 'origem': 'São Paulo', 'destino': 'Rio', 'cor': 'azul', 'tamanho': 3, ...}
        """
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
        """
        Formata uma lista de rotas.
        
        Args:
            rotas: Lista de Rota
            
        Returns:
            Lista de dicts formatados
        """
        return [EntityFormatters.formatar_rota(rota) for rota in rotas]
    
    @staticmethod
    def formatar_jogador(jogador: Jogador, incluir_cartas: bool = False, incluir_bilhetes: bool = False) -> Dict[str, Any]:
        """
        Formata informações de um jogador para resposta da API.
        
        Args:
            jogador: Instância de Jogador
            incluir_cartas: Se deve incluir cartas na mão
            incluir_bilhetes: Se deve incluir bilhetes
            
        Returns:
            Dict com informações do jogador
        """
        resultado = {
            "id": jogador.id,
            "nome": jogador.nome,
            "cor": jogador.cor.value,
            "pontos": jogador.pontuacao,
            "trens_restantes": len(jogador.vagoes),  # Número de vagões disponíveis
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
        """
        Formata uma lista de jogadores.
        
        Args:
            jogadores: Lista de Jogador
            incluir_cartas: Se deve incluir cartas na mão
            incluir_bilhetes: Se deve incluir bilhetes
            
        Returns:
            Lista de dicts formatados
        """
        return [
            EntityFormatters.formatar_jogador(jogador, incluir_cartas, incluir_bilhetes)
            for jogador in jogadores
        ]
    
    @staticmethod
    def formatar_rotas_bilhetes(bilhetes: List[BilheteDestino]) -> str:
        """
        Formata lista de bilhetes como texto de rotas compacto.
        
        Centraliza formatação duplicada em TicketPurchaseService e outros locais
        onde bilhetes precisam ser exibidos como string legível.
        
        Args:
            bilhetes: Lista de bilhetes
            
        Returns:
            String formatada: "São Paulo → Rio, Brasília → Salvador"
            Retorna string vazia se lista vazia
            
        Example:
            >>> bilhetes = [bilhete1, bilhete2]
            >>> EntityFormatters.formatar_rotas_bilhetes(bilhetes)
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
        bilhetes_escolhidos: List[BilheteDestino],
        quantidade_recusados: int
    ) -> str:
        """
        Cria mensagem formatada de compra de bilhetes.
        
        Centraliza lógica duplicada de construção de mensagem legível
        sobre bilhetes escolhidos e recusados.
        
        Args:
            jogador_nome: Nome do jogador
            bilhetes_escolhidos: Bilhetes que o jogador ficou
            quantidade_recusados: Quantidade devolvida
            
        Returns:
            Mensagem formatada e legível
            
        Example:
            >>> EntityFormatters.criar_mensagem_compra_bilhetes(
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
            rotas = EntityFormatters.formatar_rotas_bilhetes(bilhetes_escolhidos)
            mensagem += f" Bilhetes escolhidos: {rotas}."
        
        return mensagem
