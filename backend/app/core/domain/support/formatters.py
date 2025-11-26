"""
Domain-level formatting helpers.

REFATORAÇÃO DRY: Este módulo agora delega para shared/formatters.py 
para evitar duplicação de lógica de formatação.

Mantém compatibilidade com imports existentes no domínio.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ..entities.carta_vagao import CartaVagao


def format_card(carta: Any) -> Dict[str, Any]:
    """
    Format a single card dict, accepting CartaVagao or legacy dicts.
    
    REFATORAÇÃO DRY: Lógica unificada para formatar cartas de várias fontes.
    """
    if isinstance(carta, dict):
        return {
            "cor": carta.get("cor", ""),
            "eh_locomotiva": carta.get("ehLocomotiva", carta.get("eh_locomotiva", False)),
        }
    if isinstance(carta, CartaVagao):
        return {
            "cor": carta.cor.value if carta.cor else None,
            "eh_locomotiva": carta.ehLocomotiva,
        }
    return {"cor": None, "eh_locomotiva": False}


def format_cards(cartas: Iterable[Any]) -> List[Dict[str, Any]]:
    """Format a collection of cards using format_card per item."""
    return [format_card(carta) for carta in cartas]


# Re-export para compatibilidade futura - permite migração gradual para EntityFormatters
__all__ = ["format_card", "format_cards"]
