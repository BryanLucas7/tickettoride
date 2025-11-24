"""Domain-level ticket helpers (moved from shared layer)."""
from __future__ import annotations

from typing import List, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from ..entities.bilhete_destino import BilheteDestino
    from ..entities.jogador import Jogador


class BilheteHelpers:
    """Pure fabrication helpers for handling ticket selection workflows."""

    @staticmethod
    def processar_escolha_bilhetes(
        jogador: "Jogador",
        bilhetes_escolhidos: List["BilheteDestino"],
        bilhetes_recusados: List["BilheteDestino"],
        gerenciador_baralho,
    ) -> None:
        jogador.bilhetes.extend(bilhetes_escolhidos)
        if bilhetes_recusados:
            gerenciador_baralho.devolverBilhetes(bilhetes_recusados)

    @staticmethod
    def separar_bilhetes_por_indices(
        bilhetes_disponiveis: List["BilheteDestino"],
        indices_escolhidos: List[int],
    ) -> Tuple[List["BilheteDestino"], List["BilheteDestino"]]:
        indices_unicos = list(dict.fromkeys(indices_escolhidos))
        indices_set = set(indices_unicos)
        bilhetes_escolhidos = [
            bilhetes_disponiveis[indice]
            for indice in indices_unicos
            if indice < len(bilhetes_disponiveis)
        ]
        bilhetes_recusados = [
            bilhete
            for indice, bilhete in enumerate(bilhetes_disponiveis)
            if indice not in indices_set
        ]
        return bilhetes_escolhidos, bilhetes_recusados

    @staticmethod
    def validar_quantidade_minima(
        quantidade: int,
        minimo: int = 2,
        nome_contexto: str = "bilhetes",
    ) -> None:
        if quantidade < minimo:
            raise ValueError(f"Select at least {minimo} {nome_contexto}")

    @staticmethod
    def validar_quantidade_maxima(
        quantidade: int,
        maximo: int,
        nome_contexto: str = "bilhetes",
    ) -> None:
        if quantidade > maximo:
            raise ValueError(f"Cannot select more than {maximo} {nome_contexto}")

    @staticmethod
    def validar_selecao_inicial_bilhetes(
        bilhetes_ids: List,
        bilhetes_disponiveis: List["BilheteDestino"],
    ) -> None:
        BilheteHelpers.validar_quantidade_minima(len(bilhetes_ids), minimo=2, nome_contexto="tickets")
        BilheteHelpers.validar_quantidade_maxima(
            len(bilhetes_ids),
            maximo=len(bilhetes_disponiveis),
            nome_contexto="tickets than available",
        )

    @staticmethod
    def resolver_bilhetes_por_ids(
        bilhetes_disponiveis: List["BilheteDestino"],
        bilhetes_ids: List,
        remover_duplicatas: bool = True,
    ) -> List["BilheteDestino"]:
        bilhetes_resolvidos: List["BilheteDestino"] = []
        ids_uuid = {bid for bid in bilhetes_ids if isinstance(bid, str)}
        ids_objeto = {bid for bid in bilhetes_ids if isinstance(bid, int)}
        for bilhete in bilhetes_disponiveis:
            if hasattr(bilhete, "id") and bilhete.id in ids_uuid:
                if not remover_duplicatas or bilhete not in bilhetes_resolvidos:
                    bilhetes_resolvidos.append(bilhete)
            elif id(bilhete) in ids_objeto:
                if not remover_duplicatas or bilhete not in bilhetes_resolvidos:
                    bilhetes_resolvidos.append(bilhete)
        return bilhetes_resolvidos
