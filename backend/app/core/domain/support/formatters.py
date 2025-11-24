"""Domain-level formatting helpers to avoid depending on shared modules."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ..entities.carta_vagao import CartaVagao


def format_card(carta: Any) -> Dict[str, Any]:
    """Format a single card dict, accepting CartaVagao or legacy dicts."""
    if isinstance(carta, dict):
        return {
            "cor": carta.get("cor", ""),
            "eh_locomotiva": carta.get("ehLocomotiva", False),
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
