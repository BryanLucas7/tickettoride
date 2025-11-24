"""
ResponseBuilder - Pure Fabrication para padronização de respostas HTTP.

Este módulo implementa o padrão Pure Fabrication (GRASP) para centralizar
a criação de respostas HTTP em um formato consistente. Resolve o problema
de múltiplos formatos de resposta espalhados pelo sistema:
- {"sucesso": False} (português)
- {"success": False} (inglês)
- Mix de ambos

Responsabilidades:
- Criar respostas de sucesso padronizadas
- Criar respostas de erro padronizadas
- Adicionar informações de turno/fim de jogo
- Garantir formato único: {"success": bool, "message": str, ...}

Padrões aplicados:
- Pure Fabrication (GRASP): Classe artificial para responsabilidade não natural
- Creator (GRASP): Centraliza criação de estruturas de resposta

Quando usar cada método:
1. ResponseBuilder.success() - Resposta simples sem turno
2. ResponseBuilder.success_with_turn() - Ação que passa turno automaticamente
3. ResponseBuilder.error() - Resposta de erro
"""

from typing import Any, Dict, Optional


class ResponseBuilder:
    """
    Construtor de respostas HTTP padronizadas.
    
    Todas as respostas seguem o formato base:
    {
        "success": bool,
        "message": str,
        ...campos_adicionais
    }
    
    Exemplos:
        >>> ResponseBuilder.success("Ação realizada")
        {"success": True, "message": "Ação realizada"}
        
        >>> ResponseBuilder.error("Jogador não encontrado")
        {"success": False, "message": "Jogador não encontrado"}
        
        >>> ResponseBuilder.success("Carta comprada", carta={"cor": "azul"})
        {"success": True, "message": "Carta comprada", "carta": {"cor": "azul"}}
    """
    
    @staticmethod
    def success(message: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Cria uma resposta de sucesso padronizada.
        
        Args:
            message: Mensagem descritiva da ação realizada
            data: Dados adicionais a incluir na resposta (opcional)
            **kwargs: Campos adicionais a incluir na resposta
            
        Returns:
            Dicionário com formato: {"success": True, "message": str, ...}
            
        Exemplos:
            >>> ResponseBuilder.success("Rota conquistada")
            {"success": True, "message": "Rota conquistada"}
            
            >>> ResponseBuilder.success("Carta comprada", carta={"cor": "vermelho"})
            {"success": True, "message": "Carta comprada", "carta": {"cor": "vermelho"}}
            
            >>> ResponseBuilder.success("Bilhetes sorteados", data={"bilhetes": [...]})
            {"success": True, "message": "Bilhetes sorteados", "bilhetes": [...]}
        """
        response = {
            "success": True,
            "message": message
        }
        
        # Se data foi fornecido, mescla seus campos na resposta
        if data:
            response.update(data)
        
        # Adiciona campos extras fornecidos via kwargs
        if kwargs:
            response.update(kwargs)
            
        return response
    
    @staticmethod
    def error(message: str, code: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Cria uma resposta de erro padronizada.
        
        Args:
            message: Mensagem descritiva do erro
            code: Código identificador do erro (opcional)
            **kwargs: Campos adicionais a incluir na resposta
            
        Returns:
            Dicionário com formato: {"success": False, "message": str, ...}
            
        Exemplos:
            >>> ResponseBuilder.error("Jogador não encontrado")
            {"success": False, "message": "Jogador não encontrado"}
            
            >>> ResponseBuilder.error("Rota já conquistada", code="ROTA_CONQUISTADA")
            {"success": False, "message": "Rota já conquistada", "code": "ROTA_CONQUISTADA"}
            
            >>> ResponseBuilder.error("Cartas insuficientes", cartas_necessarias=3)
            {"success": False, "message": "Cartas insuficientes", "cartas_necessarias": 3}
        """
        response = {
            "success": False,
            "message": message
        }
        
        if code:
            response["code"] = code
            
        if kwargs:
            response.update(kwargs)
            
        return response
    
    @staticmethod
    def success_with_turn(
        message: str,
        resultado_turno: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Cria resposta de sucesso incluindo informações de fim de turno.
        
        Centraliza padrão duplicado em RouteConquestService, TicketPurchaseService
        e outros services que precisam passar turno automaticamente.
        
        Args:
            message: Mensagem descritiva da ação realizada
            resultado_turno: Dict retornado por GameActionService.passar_turno_e_verificar_fim()
                            Deve conter: proximo_jogador, jogo_terminou, mensagem_fim
            **kwargs: Campos específicos da ação (points, tickets_kept, etc.)
            
        Returns:
            Dict padronizado com informações de ação + turno
            
        Exemplos:
            >>> ResponseBuilder.success_with_turn(
            ...     "Rota conquistada",
            ...     resultado_turno={"proximo_jogador": "2", "jogo_terminou": False, "mensagem_fim": None},
            ...     points=4,
            ...     trains_remaining=10
            ... )
            {
                "success": True,
                "message": "Rota conquistada",
                "turn_completed": True,
                "turno_passado": True,
                "next_player": "2",
                "jogo_terminou": False,
                "mensagem_fim": None,
                "points": 4,
                "trains_remaining": 10
            }
            
            >>> ResponseBuilder.success_with_turn(
            ...     "Bilhetes comprados",
            ...     resultado_turno={"proximo_jogador": "3", "jogo_terminou": True, "mensagem_fim": "Última rodada!"},
            ...     tickets_kept=2,
            ...     tickets_returned=1
            ... )
            {
                "success": True,
                "message": "Bilhetes comprados",
                "turn_completed": True,
                "turno_passado": True,
                "next_player": "3",
                "jogo_terminou": True,
                "mensagem_fim": "Última rodada!",
                "tickets_kept": 2,
                "tickets_returned": 1
            }
        """
        response = {
            "success": True,
            "message": message,
            "turn_completed": True,
            "turno_passado": True,
            "next_player": resultado_turno["proximo_jogador"],
            "jogo_terminou": resultado_turno["jogo_terminou"],
            "mensagem_fim": resultado_turno["mensagem_fim"]
        }
        
        # Adiciona campos específicos da ação
        if kwargs:
            response.update(kwargs)
        
        return response
