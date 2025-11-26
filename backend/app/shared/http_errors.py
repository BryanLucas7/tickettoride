"""
HttpErrors - Helper centralizado para exceções HTTP.

REFATORAÇÃO DRY: Centraliza a criação de HTTPException para eliminar
padrões repetidos em ~20 lugares do código.

Padrão GRASP: Pure Fabrication
- Classe utilitária para responsabilidade de criação de exceções

Antes (código repetido):
    raise HTTPException(status_code=400, detail="Mensagem de erro")
    raise HTTPException(status_code=404, detail="Recurso não encontrado")

Depois (código centralizado):
    raise HttpErrors.bad_request("Mensagem de erro")
    raise HttpErrors.not_found("Recurso não encontrado")

Benefícios:
- Padronização de mensagens de erro
- Facilita logging centralizado
- Permite adicionar metadados consistentes
- Reduz boilerplate
"""

from typing import Optional, Any
from fastapi import HTTPException


class HttpErrors:
    """
    Helper para criação centralizada de HTTPException.
    
    Métodos estáticos retornam HTTPException já configurada,
    pronta para ser lançada com `raise`.
    
    Exemplos:
        raise HttpErrors.bad_request("Cartas inválidas")
        raise HttpErrors.not_found("Jogo", "game-123")
        raise HttpErrors.validation_error("Campo obrigatório", "player_id")
    """
    
    @staticmethod
    def bad_request(message: str, code: Optional[str] = None) -> HTTPException:
        """
        Erro 400 - Bad Request (requisição inválida).
        
        Use para:
        - Dados inválidos na requisição
        - Regras de negócio violadas
        - Ações não permitidas no estado atual
        
        Args:
            message: Mensagem descritiva do erro
            code: Código identificador opcional (ex: "CARTAS_INVALIDAS")
            
        Returns:
            HTTPException configurada para ser lançada
            
        Exemplos:
            raise HttpErrors.bad_request("Selecione exatamente 3 cartas")
            raise HttpErrors.bad_request("Rota já conquistada", code="ROTA_OCUPADA")
        """
        detail = message
        if code:
            detail = {"message": message, "code": code}
        return HTTPException(status_code=400, detail=detail)
    
    @staticmethod
    def not_found(resource: str, identifier: Optional[Any] = None) -> HTTPException:
        """
        Erro 404 - Not Found (recurso não encontrado).
        
        Use para:
        - Jogo não encontrado
        - Jogador não encontrado
        - Rota não encontrada
        
        Args:
            resource: Nome do recurso (ex: "Jogo", "Jogador", "Rota")
            identifier: ID ou identificador do recurso
            
        Returns:
            HTTPException configurada para ser lançada
            
        Exemplos:
            raise HttpErrors.not_found("Jogo", "game-123")
            raise HttpErrors.not_found("Rota", rota_id)
        """
        if identifier:
            message = f"{resource} {identifier} não encontrado"
        else:
            message = f"{resource} não encontrado"
        return HTTPException(status_code=404, detail=message)
    
    @staticmethod
    def validation_error(message: str, field: Optional[str] = None) -> HTTPException:
        """
        Erro 400 - Erro de validação.
        
        Use para erros específicos de validação de campos.
        
        Args:
            message: Mensagem do erro de validação
            field: Nome do campo com erro (opcional)
            
        Returns:
            HTTPException configurada para ser lançada
            
        Exemplos:
            raise HttpErrors.validation_error("Índice inválido", "card_index")
            raise HttpErrors.validation_error("Quantidade mínima: 2")
        """
        if field:
            detail = {"message": message, "field": field}
        else:
            detail = message
        return HTTPException(status_code=400, detail=detail)
    
    @staticmethod
    def forbidden(message: str = "Ação não permitida") -> HTTPException:
        """
        Erro 403 - Forbidden (acesso negado).
        
        Use para:
        - Ação não permitida para o jogador atual
        - Tentativa de ação fora do turno
        
        Args:
            message: Mensagem descritiva
            
        Returns:
            HTTPException configurada para ser lançada
        """
        return HTTPException(status_code=403, detail=message)
    
    @staticmethod
    def conflict(message: str, code: Optional[str] = None) -> HTTPException:
        """
        Erro 409 - Conflict (conflito de estado).
        
        Use para:
        - Recurso já existe
        - Estado incompatível para ação
        
        Args:
            message: Mensagem descritiva
            code: Código identificador opcional
            
        Returns:
            HTTPException configurada para ser lançada
            
        Exemplos:
            raise HttpErrors.conflict("Rota já conquistada")
            raise HttpErrors.conflict("Jogo já iniciado", code="JOGO_INICIADO")
        """
        detail = message
        if code:
            detail = {"message": message, "code": code}
        return HTTPException(status_code=409, detail=detail)
    
    @staticmethod
    def internal_error(message: str = "Erro interno do servidor") -> HTTPException:
        """
        Erro 500 - Internal Server Error.
        
        Use para erros inesperados que não devem expor detalhes ao cliente.
        
        Args:
            message: Mensagem genérica (não exponha detalhes internos)
            
        Returns:
            HTTPException configurada para ser lançada
        """
        return HTTPException(status_code=500, detail=message)


# Aliases convenientes para uso frequente
bad_request = HttpErrors.bad_request
not_found = HttpErrors.not_found
validation_error = HttpErrors.validation_error
forbidden = HttpErrors.forbidden
conflict = HttpErrors.conflict
internal_error = HttpErrors.internal_error
