"""Dados canônicos do mapa Ticket to Ride Brasil para o backend.

Fornece utilitário para popular o tabuleiro assim que o jogo inicia,
mantendo o arquivo frontend `app/data/mapaBrasil.ts` apenas como
fonte visual.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

try:
    from ..models.entities.cidade import Cidade
    from ..models.entities.cor import Cor
    from ..models.entities.rota import Rota
    from ..models.entities.tabuleiro import Tabuleiro
except ImportError:  # Suporte para execução quando "app" não está no caminho
    from models.cidade import Cidade
    from models.cor import Cor
    from models.rota import Rota
    from models.tabuleiro import Tabuleiro

# Lista de cidades disponíveis no mapa brasileiro
CIDADES_DATA: List[Dict[str, str]] = [
    {"id": "PORTO_ALEGRE", "nome": "Porto Alegre"},
    {"id": "BAURU", "nome": "Bauru"},
    {"id": "RIO_DE_JANEIRO", "nome": "Rio de Janeiro"},
    {"id": "BRASILIA", "nome": "Brasília"},
    {"id": "CAMPO_GRANDE", "nome": "Campo Grande"},
    {"id": "CUIABA", "nome": "Cuiabá"},
    {"id": "SALVADOR", "nome": "Salvador"},
    {"id": "RECIFE", "nome": "Recife"},
    {"id": "FORTALEZA", "nome": "Fortaleza"},
    {"id": "BELEM", "nome": "Belém"},
    {"id": "MANAUS", "nome": "Manaus"},
    {"id": "RIO_BRANCO", "nome": "Rio Branco"},
    {"id": "PALMAS", "nome": "Palmas"},
]

# Rotas conforme adaptação brasileira
ROTAS_DATA: List[Dict[str, object]] = [
    {"id": "R01", "cidadeA": "PORTO_ALEGRE", "cidadeB": "BAURU", "cor": "VERDE", "comprimento": 4},
    {"id": "R02", "cidadeA": "PORTO_ALEGRE", "cidadeB": "CAMPO_GRANDE", "cor": "AMARELO", "comprimento": 4},
    {"id": "R03", "cidadeA": "BAURU", "cidadeB": "BRASILIA", "cor": "VERMELHO", "comprimento": 3},
    {"id": "R04", "cidadeA": "BAURU", "cidadeB": "RIO_DE_JANEIRO", "cor": "AZUL", "comprimento": 3},
    {"id": "R05", "cidadeA": "BAURU", "cidadeB": "CAMPO_GRANDE", "cor": "PRETO", "comprimento": 2},
    {"id": "R06", "cidadeA": "RIO_DE_JANEIRO", "cidadeB": "SALVADOR", "cor": "AMARELO", "comprimento": 4},
    {"id": "R07", "cidadeA": "RIO_DE_JANEIRO", "cidadeB": "BRASILIA", "cor": "ROXO", "comprimento": 3},
    {"id": "R08", "cidadeA": "CAMPO_GRANDE", "cidadeB": "CUIABA", "cor": "LARANJA", "comprimento": 3},
    {"id": "R09", "cidadeA": "CAMPO_GRANDE", "cidadeB": "BRASILIA", "cor": "CINZA", "comprimento": 3},
    {"id": "R09B", "cidadeA": "CUIABA", "cidadeB": "BRASILIA", "cor": "PRETO", "comprimento": 4},
    {"id": "R10", "cidadeA": "PALMAS", "cidadeB": "BRASILIA", "cor": "VERDE", "comprimento": 3},
    {"id": "R11", "cidadeA": "PALMAS", "cidadeB": "CUIABA", "cor": "AMARELO", "comprimento": 5},
    {"id": "R12", "cidadeA": "PALMAS", "cidadeB": "MANAUS", "cor": "ROXO", "comprimento": 6},
    {"id": "R13", "cidadeA": "PALMAS", "cidadeB": "BELEM", "cor": "VERMELHO", "comprimento": 5},
    {"id": "R14", "cidadeA": "PALMAS", "cidadeB": "FORTALEZA", "cor": "PRETO", "comprimento": 5},
    {"id": "R15", "cidadeA": "PALMAS", "cidadeB": "RECIFE", "cor": "AZUL", "comprimento": 5},
    {"id": "R16", "cidadeA": "PALMAS", "cidadeB": "SALVADOR", "cor": "LARANJA", "comprimento": 4},
    {"id": "R17", "cidadeA": "BRASILIA", "cidadeB": "SALVADOR", "cor": "VERDE", "comprimento": 4},
    {"id": "R18", "cidadeA": "SALVADOR", "cidadeB": "RECIFE", "cor": "CINZA", "comprimento": 4},
    {"id": "R19", "cidadeA": "RECIFE", "cidadeB": "FORTALEZA", "cor": "CINZA", "comprimento": 2},
    {"id": "R20", "cidadeA": "FORTALEZA", "cidadeB": "BELEM", "cor": "CINZA", "comprimento": 5},
    {"id": "R21", "cidadeA": "BELEM", "cidadeB": "MANAUS", "cor": "CINZA", "comprimento": 6},
    {"id": "R22", "cidadeA": "MANAUS", "cidadeB": "CUIABA", "cor": "CINZA", "comprimento": 5},
    {"id": "R23", "cidadeA": "RIO_BRANCO", "cidadeB": "MANAUS", "cor": "LARANJA", "comprimento": 5},
    {"id": "R24", "cidadeA": "RIO_BRANCO", "cidadeB": "CUIABA", "cor": "CINZA", "comprimento": 5},
]

_COR_MAP: Dict[str, Cor] = {
    "VERMELHO": Cor.VERMELHO,
    "AZUL": Cor.AZUL,
    "VERDE": Cor.VERDE,
    "AMARELO": Cor.AMARELO,
    "PRETO": Cor.PRETO,
    "LARANJA": Cor.LARANJA,
    "ROXO": Cor.ROXO,
    "BRANCO": Cor.BRANCO,
    "CINZA": Cor.CINZA,
}


def carregar_tabuleiro_brasil(tabuleiro: Tabuleiro) -> Dict[str, object]:
    """Popula o tabuleiro com cidades e rotas brasileiras.

    A função só insere dados se o tabuleiro estiver vazio, permitindo testes
    customizados que configurem mapas alternativos.
    """

    if tabuleiro.cidades and tabuleiro.rotas:
        return {
            "cidades": len(tabuleiro.cidades),
            "rotas": len(tabuleiro.rotas),
            "rotas_duplas": _identificar_rotas_duplas(),
        }

    tabuleiro.cidades.clear()
    tabuleiro.rotas.clear()

    for cidade_data in CIDADES_DATA:
        tabuleiro.cidades.append(Cidade(**cidade_data))

    cidades_por_id = {cidade.id: cidade for cidade in tabuleiro.cidades}

    for rota_data in ROTAS_DATA:
        cor = rota_data["cor"]
        rota = Rota(
            id=rota_data["id"],
            cidadeA=cidades_por_id[rota_data["cidadeA"]],
            cidadeB=cidades_por_id[rota_data["cidadeB"]],
            cor=_COR_MAP[cor],
            comprimento=int(rota_data["comprimento"]),
        )
        tabuleiro.rotas.append(rota)

    return {
        "cidades": len(tabuleiro.cidades),
        "rotas": len(tabuleiro.rotas),
        "rotas_duplas": _identificar_rotas_duplas(),
    }


def _identificar_rotas_duplas() -> List[Tuple[str, str]]:
    """Identifica rotas paralelas (cidades iguais porém IDs diferentes)."""

    agrupado: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    for rota in ROTAS_DATA:
        chave = tuple(sorted((rota["cidadeA"], rota["cidadeB"])))
        agrupado[chave].append(rota["id"])

    return [tuple(ids) for ids in agrupado.values() if len(ids) > 1]
