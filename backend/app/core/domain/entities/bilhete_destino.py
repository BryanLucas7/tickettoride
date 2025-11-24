from dataclasses import dataclass
from .cidade import Cidade, CIDADES
from .carta import Carta

@dataclass
class BilheteDestino(Carta):
    cidadeOrigem: Cidade = None
    cidadeDestino: Cidade = None
    pontos: int = 0

    def __repr__(self):
        if self.cidadeOrigem and self.cidadeDestino:
            return f"<Bilhete {self.cidadeOrigem.id} -> {self.cidadeDestino.id} ({self.pontos})>"
        return f"<Bilhete ({self.pontos})>"


# 🔽 Função auxiliar para buscar cidade por ID
def get_cidade(id: str) -> Cidade:
    for c in CIDADES:
        if c.id == id:
            return c
    raise ValueError(f"Cidade '{id}' não encontrada em CIDADES.")


# 🎯 30 cartas de destino — Ticket to Ride: Brasil
BILHETES_DESTINO: list[BilheteDestino] = [
    BilheteDestino(cidadeOrigem=get_cidade("PORTO_ALEGRE"), cidadeDestino=get_cidade("BAURU"), pontos=5),
    BilheteDestino(cidadeOrigem=get_cidade("PORTO_ALEGRE"), cidadeDestino=get_cidade("CAMPO_GRANDE"), pontos=7),
    BilheteDestino(cidadeOrigem=get_cidade("PORTO_ALEGRE"), cidadeDestino=get_cidade("BRASILIA"), pontos=10),
    BilheteDestino(cidadeOrigem=get_cidade("PORTO_ALEGRE"), cidadeDestino=get_cidade("RIO_DE_JANEIRO"), pontos=11),
    BilheteDestino(cidadeOrigem=get_cidade("BAURU"), cidadeDestino=get_cidade("CAMPO_GRANDE"), pontos=4),
    BilheteDestino(cidadeOrigem=get_cidade("BAURU"), cidadeDestino=get_cidade("BRASILIA"), pontos=6),
    BilheteDestino(cidadeOrigem=get_cidade("BAURU"), cidadeDestino=get_cidade("RIO_DE_JANEIRO"), pontos=6),
    BilheteDestino(cidadeOrigem=get_cidade("BAURU"), cidadeDestino=get_cidade("SALVADOR"), pontos=10),
    BilheteDestino(cidadeOrigem=get_cidade("BRASILIA"), cidadeDestino=get_cidade("SALVADOR"), pontos=7),
    BilheteDestino(cidadeOrigem=get_cidade("BRASILIA"), cidadeDestino=get_cidade("RECIFE"), pontos=11),
    BilheteDestino(cidadeOrigem=get_cidade("BRASILIA"), cidadeDestino=get_cidade("FORTALEZA"), pontos=12),
    BilheteDestino(cidadeOrigem=get_cidade("BRASILIA"), cidadeDestino=get_cidade("BELEM"), pontos=13),
    BilheteDestino(cidadeOrigem=get_cidade("BRASILIA"), cidadeDestino=get_cidade("MANAUS"), pontos=14),
    BilheteDestino(cidadeOrigem=get_cidade("BRASILIA"), cidadeDestino=get_cidade("RIO_BRANCO"), pontos=15),
    BilheteDestino(cidadeOrigem=get_cidade("CAMPO_GRANDE"), cidadeDestino=get_cidade("CUIABA"), pontos=5),
    BilheteDestino(cidadeOrigem=get_cidade("CAMPO_GRANDE"), cidadeDestino=get_cidade("BRASILIA"), pontos=5),
    BilheteDestino(cidadeOrigem=get_cidade("CAMPO_GRANDE"), cidadeDestino=get_cidade("SALVADOR"), pontos=10),
    BilheteDestino(cidadeOrigem=get_cidade("CUIABA"), cidadeDestino=get_cidade("PALMAS"), pontos=6),
    BilheteDestino(cidadeOrigem=get_cidade("CUIABA"), cidadeDestino=get_cidade("MANAUS"), pontos=10),
    BilheteDestino(cidadeOrigem=get_cidade("CUIABA"), cidadeDestino=get_cidade("RIO_BRANCO"), pontos=8),
    BilheteDestino(cidadeOrigem=get_cidade("PALMAS"), cidadeDestino=get_cidade("BELEM"), pontos=6),
    BilheteDestino(cidadeOrigem=get_cidade("PALMAS"), cidadeDestino=get_cidade("FORTALEZA"), pontos=7),
    BilheteDestino(cidadeOrigem=get_cidade("PALMAS"), cidadeDestino=get_cidade("RECIFE"), pontos=7),
    BilheteDestino(cidadeOrigem=get_cidade("PALMAS"), cidadeDestino=get_cidade("SALVADOR"), pontos=6),
    BilheteDestino(cidadeOrigem=get_cidade("SALVADOR"), cidadeDestino=get_cidade("RECIFE"), pontos=5),
    BilheteDestino(cidadeOrigem=get_cidade("SALVADOR"), cidadeDestino=get_cidade("FORTALEZA"), pontos=8),
    BilheteDestino(cidadeOrigem=get_cidade("RECIFE"), cidadeDestino=get_cidade("FORTALEZA"), pontos=4),
    BilheteDestino(cidadeOrigem=get_cidade("BELEM"), cidadeDestino=get_cidade("MANAUS"), pontos=10),
    BilheteDestino(cidadeOrigem=get_cidade("BELEM"), cidadeDestino=get_cidade("FORTALEZA"), pontos=7),
    BilheteDestino(cidadeOrigem=get_cidade("RIO_BRANCO"), cidadeDestino=get_cidade("MANAUS"), pontos=6),
]
