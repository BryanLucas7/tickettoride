"""
Service para seleção de bilhetes iniciais.

Extrai lógica complexa do endpoint escolher_bilhetes_iniciais em ticket_routes.py.

Responsabilidades:
- Validar existência de bilhetes pendentes
- Validar quantidade mínima/máxima de bilhetes selecionados (via BilheteHelpers)
- Resolver identificadores flexíveis (ID ou object ID) (via BilheteHelpers)
- Chamar JogoBilhetesService para processar escolha
- Construir response formatado para API

GRASP:
- Single Responsibility: Apenas seleção inicial de bilhetes
- Information Expert: Conhece regras de validação de bilhetes iniciais
- DRY: Usa BilheteHelpers para eliminar duplicação de validações
"""
from typing import Dict, Any, List
from ...core.domain.entities.jogo import Jogo
from ...core.domain.entities.jogador import Jogador
from ...shared.response_builder import ResponseBuilder
from ...shared.formatters import EntityFormatters
from ...shared.bilhete_helpers import BilheteHelpers


class TicketSelectionService:
    @staticmethod
    def escolher_bilhetes_iniciais(
        jogo: Jogo, 
        player_id: str, 
        bilhetes_ids: List[Any], 
        jogador: Jogador
    ) -> Dict[str, Any]:
        """
        Processa escolha de bilhetes iniciais e retorna response pronto para API.
        
        Args:
            jogo: Instância do jogo
            player_id: ID do jogador (str)
            bilhetes_ids: Lista de IDs selecionados (str/int/object)
            jogador: Instância do Jogador
            
        Returns:
            Dict compatível com EscolhaBilhetesIniciaisResponse
            {"success": bool, "message": str|None, "player_id": str, "tickets_kept": int, ...}
        """
        bilhetes_pendentes = jogo.bilhetesPendentesEscolha.get(jogador.id)
        if not bilhetes_pendentes:
            return ResponseBuilder.error("No pending initial ticket selection for this player")

        # Validações centralizadas via BilheteHelpers
        try:
            BilheteHelpers.validar_selecao_inicial_bilhetes(bilhetes_ids, bilhetes_pendentes)
        except ValueError as e:
            return ResponseBuilder.error(str(e))

        # Resolve IDs para bilhetes (sem duplicatas)
        bilhetes_aceitos = BilheteHelpers.resolver_bilhetes_por_ids(
            bilhetes_pendentes, 
            bilhetes_ids, 
            remover_duplicatas=True
        )

        # Valida que resolveu bilhetes suficientes após remoção de duplicatas
        if len(bilhetes_aceitos) < 2:
            return ResponseBuilder.error("Selection must include at least two valid tickets")

        bilhetes_recusados = [b for b in bilhetes_pendentes if b not in bilhetes_aceitos]

        # Chama processamento interno do jogo
        sucesso = jogo.escolherBilhetesIniciais(jogador.id, bilhetes_ids)
        if not sucesso:
            return ResponseBuilder.error("Invalid ticket selection")

        # Bilhetes formatados para response
        bilhetes_formatados = EntityFormatters.formatar_bilhetes(bilhetes_aceitos)

        return ResponseBuilder.success(
            "Bilhetes iniciais selecionados com sucesso",
            player_id=str(jogador.id),
            tickets_kept=len(bilhetes_aceitos),
            tickets_returned=len(bilhetes_recusados),
            bilhetes=bilhetes_formatados
        )