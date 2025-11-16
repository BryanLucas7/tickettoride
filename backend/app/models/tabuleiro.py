from dataclasses import dataclass, field
from typing import List, Optional

# Import local types lazily to avoid circulars during typing
from .validador_rotas_duplas import ValidadorRotasDuplas
from .cidade import Cidade
from .rota import Rota

@dataclass
class Tabuleiro:
    cidades: List[Cidade] = field(default_factory=list)
    rotas: List[Rota] = field(default_factory=list)
    validador_duplas: Optional[ValidadorRotasDuplas] = None

    def obterRotasDisponiveis(self, rota) -> List[Rota]:
        """Retorna todas as rotas disponíveis (não reivindicadas)"""
        return [r for r in self.rotas if r.proprietario is None]

    def obterDisponiveisRota(self, rota) -> bool:
        """Verifica se uma rota específica está disponível"""
        for r in self.rotas:
            if r.id == rota.id:
                return r.proprietario is None
        return False

    def obterCidadesNaCidade(self, cidade: Cidade) -> List[Cidade]:
        """Retorna todas as cidades conectadas a uma cidade específica"""
        cidades_conectadas = []
        for rota in self.rotas:
            if rota.cidadeA.id == cidade.id:
                cidades_conectadas.append(rota.cidadeB)
            elif rota.cidadeB.id == cidade.id:
                cidades_conectadas.append(rota.cidadeA)
        return cidades_conectadas

    def obterRotaPorId(self, id_rota: str) -> Optional[Rota]:
        """Busca uma rota pelo ID"""
        for r in self.rotas:
            if r.id == id_rota:
                return r
        return None

    def obterCidade(self, id_cidade: str) -> Optional[Cidade]:
        """Busca uma cidade pelo ID"""
        for c in self.cidades:
            if c.id == id_cidade:
                return c
        return None
