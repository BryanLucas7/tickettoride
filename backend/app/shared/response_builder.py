"""
ResponseBuilder - Pure Fabrication para padronização de respostas HTTP.

Este módulo implementa o padrão Pure Fabrication (GRASP) para centralizar
a criação de respostas HTTP em um formato consistente. Resolve o problema
de múltiplos formatos de resposta espalhados pelo sistema:
- {"sucesso": False} (português)
- {"success": False} (inglês)
- Mix de ambos

REFATORAÇÃO DRY: Este módulo agora usa as funções base de 
core/domain/support/responses.py para evitar duplicação.

Responsabilidades:
- Criar respostas de sucesso padronizadas
- Criar respostas de erro padronizadas
- Adicionar informações de turno/fim de jogo
- Garantir formato único: {"success": bool, "message": str, ...}

Padrões aplicados:
- Pure Fabrication (GRASP): Classe artificial para responsabilidade não natural
- Creator (GRASP): Centraliza criação de estruturas de resposta
- Protected Variations (GRASP): Usa TypedDict para contratos explícitos

Quando usar cada método:
1. ResponseBuilder.success() - Resposta simples sem turno
2. ResponseBuilder.success_with_turn() - Ação que passa turno automaticamente
3. ResponseBuilder.error() - Resposta de erro
"""

from typing import Any, Dict, Optional

from ..core.domain.support.responses import (
    success_response as _base_success,
    error_response as _base_error,
)
from ..core.domain.support.types import ResultadoTurno


class ResponseBuilder:
    """
    Construtor de respostas HTTP padronizadas.
    
    REFATORAÇÃO DRY: Delega para funções base em core/domain/support/responses.py
    
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
        
        REFATORAÇÃO DRY: Delega para _base_success de core/domain/support/responses.py
        
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
        # Mescla data e kwargs
        all_kwargs = {}
        if data:
            all_kwargs.update(data)
        if kwargs:
            all_kwargs.update(kwargs)
        
        return _base_success(message, **all_kwargs)
    
    @staticmethod
    def error(message: str, code: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Cria uma resposta de erro padronizada.
        
        REFATORAÇÃO DRY: Delega para _base_error de core/domain/support/responses.py
        
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
        if code:
            kwargs["code"] = code
            
        return _base_error(message, **kwargs)
    
    @staticmethod
    def success_with_turn(
        message: str,
        resultado_turno: ResultadoTurno,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Cria resposta de sucesso incluindo informações de fim de turno.
        
        REFATORAÇÃO DRY: Usa _base_success como base e adiciona campos de turno.
        
        Centraliza padrão duplicado em RouteConquestService, TicketPurchaseService
        e outros services que precisam passar turno automaticamente.
        
        Args:
            message: Mensagem descritiva da ação realizada
            resultado_turno: Tipado como ResultadoTurno (TypedDict) para garantir
                            contrato explícito. Deve conter: proximo_jogador, 
                            jogo_terminou, mensagem_fim
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
        """
        # Campos específicos de turno
        turn_kwargs = {
            "turn_completed": True,
            "turno_passado": True,
            "next_player": resultado_turno["proximo_jogador"],
            "jogo_terminou": resultado_turno["jogo_terminou"],
            "mensagem_fim": resultado_turno["mensagem_fim"],
        }
        
        # Mescla campos de turno com kwargs adicionais
        turn_kwargs.update(kwargs)
        
        return _base_success(message, **turn_kwargs)
