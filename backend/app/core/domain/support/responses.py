"""Domain-level helpers for building and normalizing service results.

These utilities live inside the core layer so that domain services do not
need to import helpers from outer layers (e.g., app.shared).
"""
from __future__ import annotations

from typing import Any, Dict


def normalize_result(resultado: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize legacy keys to the new format."""
    if "sucesso" in resultado:
        normalizado = {
            "success": resultado["sucesso"],
            "message": resultado.get("mensagem", ""),
        }
        for chave, valor in resultado.items():
            if chave not in ("sucesso", "mensagem"):
                normalizado[chave] = valor
        return normalizado
    return resultado


def success_response(message: str, **kwargs: Any) -> Dict[str, Any]:
    """Build a success payload for domain consumers."""
    response: Dict[str, Any] = {"success": True, "message": message}
    if kwargs:
        response.update(kwargs)
    return response


def error_response(message: str, **kwargs: Any) -> Dict[str, Any]:
    """Build an error payload for domain consumers."""
    response: Dict[str, Any] = {"success": False, "message": message}
    if kwargs:
        response.update(kwargs)
    return response
