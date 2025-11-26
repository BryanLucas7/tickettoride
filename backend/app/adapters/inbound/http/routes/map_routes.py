"""
Endpoint público para expor a definição canônica do mapa.

Responsabilidade:
- Servir cidades e rotas diretamente da fonte única do backend
- Evitar que o frontend mantenha cópias duplicadas de dados de domínio
"""

from fastapi import APIRouter

from .....adapters.outbound.data.mapa_brasil import CIDADES_DATA, ROTAS_DATA
from .....core.domain.entities.cor import Cor

router = APIRouter()


def _normalizar_cor(cor_raw: str) -> str:
    """
    Converte a cor declarada no arquivo canônico para o valor do enum (lowercase).
    Mantém compatibilidade caso apareça uma cor não mapeada.
    """
    try:
        return Cor[cor_raw].value
    except KeyError:
        return str(cor_raw).lower()


@router.get("/config")
def get_map_config():
    """
    Retorna a configuração do mapa Brasil (cidades e rotas).

    Estrutura:
    - cidades: [{id, nome}]
    - rotas: [{id, cidadeA, cidadeB, cor, comprimento}]
    """
    rotas = [
        {
            "id": rota["id"],
            "cidadeA": rota["cidadeA"],
            "cidadeB": rota["cidadeB"],
            "cor": _normalizar_cor(str(rota["cor"])),
            "comprimento": int(rota["comprimento"]),
        }
        for rota in ROTAS_DATA
    ]

    return {
        "map_id": "brasil",
        "cidades": CIDADES_DATA,
        "rotas": rotas,
    }
