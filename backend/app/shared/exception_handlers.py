"""
Exception Handlers - Decorators para tratamento centralizado de exceções

Refatoração DRY: Elimina código duplicado de try/except em services e endpoints.

ANTES (Duplicação em ~10+ lugares):
    try:
        resultado = alguma_operacao()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise  # Re-raise HTTPException sem modificar

DEPOIS (Centralizado):
    @handle_validation_errors
    def alguma_operacao():
        # Lógica sem try/except
        ...
"""

from functools import wraps
from fastapi import HTTPException
from typing import Callable, TypeVar, Any

T = TypeVar('T')


def handle_validation_errors(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator que converte exceções de validação em HTTPException.
    
    Conversões:
    - ValueError → HTTPException(400, detail=str(error))
    - HTTPException → re-raise sem modificar
    - Outras exceções → propagam normalmente
    
    Uso em services:
        @handle_validation_errors
        def comprar_bilhetes(self, jogo, jogador, indices):
            # Se houver ValueError, será convertido automaticamente
            GameValidators.validar_indices(indices, ...)
            ...
    
    Uso em endpoints:
        @router.post("/...")
        @handle_validation_errors
        def endpoint(jogo: Jogo = Depends(...)):
            # ValueError de services vira HTTPException(400)
            service.operacao()
            ...
    
    Args:
        func: Função a ser decorada
        
    Returns:
        Função decorada com tratamento de exceções
        
    Examples:
        >>> @handle_validation_errors
        ... def validar_idade(idade: int):
        ...     if idade < 0:
        ...         raise ValueError("Idade não pode ser negativa")
        ...     return idade
        >>> 
        >>> validar_idade(-5)  # Raises HTTPException(400)
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return func(*args, **kwargs)
        except HTTPException:
            # Re-raise HTTPException sem modificar
            # (já tem status code e detail corretos)
            raise
        except ValueError as e:
            # Converte ValueError em HTTPException(400)
            # Assume que ValueError indica erro de validação do usuário
            raise HTTPException(status_code=400, detail=str(e))
    
    return wrapper

