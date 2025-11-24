"""
JogoBilhetesService - Responsável pelo gerenciamento de bilhetes de destino.

Refatoração DRY:
- Usa BilheteHelpers para eliminar duplicação com TicketPurchaseService
- Usa validações centralizadas de BilheteHelpers
"""

from typing import List

from ..support.bilhete_helpers import BilheteHelpers


class JogoBilhetesService:
    """Responsável pelo gerenciamento de bilhetes de destino."""

    def __init__(self, jogo):
        self.jogo = jogo

    def escolherBilhetesIniciais(self, jogador_id: str, bilhetes_escolhidos_ids: List[object]) -> bool:
        """Processa a escolha de bilhetes iniciais de um jogador

        Args:
            jogador_id: ID do jogador (UUID string)
            bilhetes_escolhidos_ids: IDs dos bilhetes que o jogador deseja FICAR (mínimo 2)

        Returns:
            True se a escolha foi válida e processada
        """
        # Verifica se o jogador tem bilhetes pendentes
        if jogador_id not in self.jogo.bilhetesPendentesEscolha:
            print(f"❌ Jogador {jogador_id} não tem bilhetes pendentes de escolha")
            return False

        bilhetes_pendentes = self.jogo.bilhetesPendentesEscolha[jogador_id]

        # Validações centralizadas via BilheteHelpers
        try:
            BilheteHelpers.validar_selecao_inicial_bilhetes(
                bilhetes_escolhidos_ids, 
                bilhetes_pendentes
            )
        except ValueError as e:
            print(f"❌ Validação falhou: {e}")
            return False

        # Resolve IDs para bilhetes (sem duplicatas)
        bilhetes_aceitos = BilheteHelpers.resolver_bilhetes_por_ids(
            bilhetes_pendentes,
            bilhetes_escolhidos_ids,
            remover_duplicatas=True
        )

        # Valida que resolveu bilhetes suficientes
        if len(bilhetes_aceitos) < 2:
            print(f"❌ Jogador deve manter pelo menos 2 bilhetes válidos (selecionou {len(bilhetes_aceitos)})")
            return False
        
        bilhetes_recusados = [b for b in bilhetes_pendentes if b not in bilhetes_aceitos]

        # Busca jogador
        jogador = self.jogo.buscarJogador(jogador_id)
        if not jogador:
            print(f"❌ Jogador {jogador_id} não encontrado")
            return False

        # Processa escolha usando helper centralizado (elimina duplicação)
        BilheteHelpers.processar_escolha_bilhetes(
            jogador,
            bilhetes_aceitos,
            bilhetes_recusados,
            self.jogo.gerenciadorDeBaralho
        )

        # Remove os bilhetes pendentes deste jogador
        del self.jogo.bilhetesPendentesEscolha[jogador_id]

        print(f"✅ Jogador {jogador_id} escolheu {len(bilhetes_aceitos)} bilhetes, recusou {len(bilhetes_recusados)}")
        return True