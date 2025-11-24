"""Domain-scoped helpers for card operations."""
from __future__ import annotations

from typing import List, Optional, Tuple, Any


def encontrar_carta_por_cor(cartas: List[Any], cor: str) -> Tuple[Optional[int], Optional[Any]]:
    """Return the first card matching the provided color (supports locomotivas)."""
    import logging
    logger = logging.getLogger(__name__)
    
    cor_normalizada = cor.lower()
    logger.info(f"🔍 DEBUG encontrar_carta - Procurando cor: '{cor_normalizada}'")
    
    for idx, carta in enumerate(cartas):
        eh_locomotiva = getattr(carta, "ehLocomotiva", False)
        cor_carta = getattr(getattr(carta, "cor", None), "value", None)
        
        logger.info(f"  Carta {idx}: ehLocomotiva={eh_locomotiva}, cor={cor_carta}")
        
        if eh_locomotiva and cor_normalizada == "locomotiva":
            logger.info(f"  ✅ Encontrou locomotiva no índice {idx}")
            return idx, carta
        if hasattr(carta, "cor") and cor_carta == cor_normalizada:
            logger.info(f"  ✅ Encontrou {cor_normalizada} no índice {idx}")
            return idx, carta
    
    logger.warning(f"  ❌ Cor '{cor_normalizada}' não encontrada")
    return None, None


def remover_cartas_por_cores(cartas: List[Any], cores: List[str]) -> List[Any]:
    """Remove cards matching the requested colors from the provided list."""
    import logging
    logger = logging.getLogger(__name__)
    
    # Debug: mostra estado atual
    cores_na_mao = [
        "locomotiva" if getattr(c, "ehLocomotiva", False) else getattr(getattr(c, "cor", None), "value", None)
        for c in cartas
    ]
    logger.info(f"🔍 DEBUG remover_cartas - Cores solicitadas: {cores}")
    logger.info(f"🔍 DEBUG remover_cartas - Cores na mão: {cores_na_mao}")
    
    cartas_removidas: List[Any] = []
    for cor in cores:
        idx, carta = encontrar_carta_por_cor(cartas, cor)
        if carta is None:
            cores_disponiveis = [
                "locomotiva" if getattr(c, "ehLocomotiva", False) else getattr(getattr(c, "cor", None), "value", None)
                for c in cartas
            ]
            raise ValueError(
                f"Carta da cor '{cor}' não encontrada. Cartas disponíveis: {cores_disponiveis}"
            )
        cartas.pop(idx)
        cartas_removidas.append(carta)
    return cartas_removidas
