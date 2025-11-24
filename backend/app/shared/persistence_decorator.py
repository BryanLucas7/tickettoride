"""
Decorator para auto-persistência de jogos após operações.

Padrão GRASP: Pure Fabrication
- Elimina duplicação de game_service.save_game() em 9+ lugares
- Garante persistência consistente após cada operação
- Centraliza lógica de salvamento em um único ponto

ANTES (duplicado em 9 endpoints):
    @router.post("/games/{game_id}/action")
    def action(
        game_id: str,
        jogo: Jogo = Depends(get_validated_game),
        game_service: GameService = Depends(get_game_service)
    ):
        resultado = service.operacao(jogo)
        game_service.save_game(game_id, jogo)  # ❌ Duplicado!
        return resultado

DEPOIS (centralizado):
    @router.post("/games/{game_id}/action")
    @auto_save_game
    def action(
        game_id: str,
        jogo: Jogo = Depends(get_validated_game),
        game_service: GameService = Depends(get_game_service)
    ):
        resultado = service.operacao(jogo)
        return resultado  # ✅ Salvo automaticamente!

Benefícios:
- DRY: Um único lugar para lógica de persistência
- Consistência: Impossível esquecer de salvar
- Manutenibilidade: Fácil adicionar logging, transações, etc.
- Testabilidade: Pode ser desabilitado em testes
"""

from functools import wraps
from typing import Callable, TypeVar, Any
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


def auto_save_game(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator que salva o jogo automaticamente após operação bem-sucedida.
    
    Detecta automaticamente os parâmetros game_id, jogo e game_service
    nas kwargs do endpoint e salva após execução sem erros.
    
    Funciona com endpoints síncronos do FastAPI que usam Depends() para
    injetar game_id, jogo e game_service.
    
    Args:
        func: Função de endpoint a ser decorada
        
    Returns:
        Função decorada com auto-salvamento
        
    Raises:
        Qualquer exceção da função original (sem modificar)
        
    Example:
        >>> @router.post("/games/{game_id}/next-turn")
        >>> @auto_save_game
        >>> def next_turn(
        ...     game_id: str,
        ...     jogo: Jogo = Depends(get_validated_game),
        ...     game_service: GameService = Depends(get_game_service),
        ...     action_service: GameActionService = Depends(get_game_action_service)
        ... ):
        ...     return action_service.passar_turno_e_verificar_fim(jogo)
        ...     # Jogo salvo automaticamente após retorno!
    
    Note:
        - Salva apenas se execução for bem-sucedida (sem exceções)
        - Requer que endpoint tenha parâmetros: game_id, jogo, game_service
        - Se algum parâmetro estiver ausente, apenas loga warning (não falha)
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # Executa função original
        result = func(*args, **kwargs)
        
        # Extrai dependências injetadas pelo FastAPI
        game_id = kwargs.get('game_id')
        jogo = kwargs.get('jogo')
        game_service = kwargs.get('game_service')
        
        # Se não encontrou diretamente, verifica se tem contexto (ctx)
        ctx = kwargs.get('ctx')
        if ctx and hasattr(ctx, 'game_id') and hasattr(ctx, 'jogo') and hasattr(ctx, 'game_service'):
            game_id = game_id or ctx.game_id
            jogo = jogo or ctx.jogo
            game_service = game_service or ctx.game_service
        
        # Valida presença de todas as dependências necessárias
        if game_id and jogo and game_service:
            try:
                game_service.save_game(game_id, jogo)
                logger.debug(f"Jogo {game_id} salvo automaticamente por @auto_save_game")
            except Exception as e:
                # Loga erro mas não falha a operação (jogo já foi processado)
                logger.error(f"Erro ao salvar jogo {game_id} automaticamente: {e}")
                # Em produção, considere re-raise se persistência é crítica
        else:
            # Apenas warning: decorator pode estar em endpoint sem essas dependências
            missing = []
            if not game_id:
                missing.append('game_id')
            if not jogo:
                missing.append('jogo')
            if not game_service:
                missing.append('game_service')
            
            logger.warning(
                f"@auto_save_game não pôde salvar jogo em {func.__name__}: "
                f"parâmetros ausentes: {', '.join(missing)}"
            )
        
        return result
    
    return wrapper

