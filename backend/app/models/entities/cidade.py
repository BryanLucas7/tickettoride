from dataclasses import dataclass

@dataclass
class Cidade:
    id: str
    nome: str

    def __repr__(self):
        return f"<Cidade {self.id} - {self.nome}>"

# 🗺️ Lista de cidades do Ticket to Ride: Brasil
CIDADES: list[Cidade] = [
    Cidade("PORTO_ALEGRE", "Porto Alegre"),
    Cidade("BAURU", "Bauru"),
    Cidade("RIO_DE_JANEIRO", "Rio de Janeiro"),
    Cidade("BRASILIA", "Brasília"),
    Cidade("CAMPO_GRANDE", "Campo Grande"),
    Cidade("CUIABA", "Cuiabá"),
    Cidade("SALVADOR", "Salvador"),
    Cidade("RECIFE", "Recife"),
    Cidade("FORTALEZA", "Fortaleza"),
    Cidade("BELEM", "Belém"),
    Cidade("MANAUS", "Manaus"),
    Cidade("RIO_BRANCO", "Rio Branco"),
    Cidade("PALMAS", "Palmas"),
]

# 🔎 Dicionário auxiliar (opcional)
CIDADES_POR_ID = {c.id: c for c in CIDADES}

def get_cidade(id: str) -> Cidade:
    """
    Retorna uma instância de Cidade pelo ID.
    Lança erro se o ID for inválido.
    """
    try:
        return CIDADES_POR_ID[id]
    except KeyError:
        raise ValueError(f"Cidade '{id}' não encontrada.")
