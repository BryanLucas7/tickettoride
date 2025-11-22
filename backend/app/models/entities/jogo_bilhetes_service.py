from typing import List
from ..entities.bilhete_destino import BilheteDestino


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
            print(f" Jogador {jogador_id} não tem bilhetes pendentes de escolha")
            return False

        # Verifica se escolheu pelo menos 2 bilhetes
        if len(bilhetes_escolhidos_ids) < 2:
            print(f" Jogador deve escolher pelo menos 2 bilhetes (escolheu {len(bilhetes_escolhidos_ids)})")
            return False

        # Verifica se escolheu no máximo 3 bilhetes
        if len(bilhetes_escolhidos_ids) > 3:
            print(f" Jogador pode escolher no máximo 3 bilhetes (escolheu {len(bilhetes_escolhidos_ids)})")
            return False

        bilhetes_pendentes = self.jogo.bilhetesPendentesEscolha[jogador_id]

        ids_objeto = {valor for valor in bilhetes_escolhidos_ids if isinstance(valor, int)}
        ids_uuid = {
            valor
            for valor in bilhetes_escolhidos_ids
            if isinstance(valor, str)
        }

        # Separa bilhetes escolhidos e recusados
        bilhetes_aceitos = [
            b
            for b in bilhetes_pendentes
            if id(b) in ids_objeto or (hasattr(b, "id") and b.id in ids_uuid)
        ]

        if len(bilhetes_aceitos) < 2:
            print(f" Jogador deve manter pelo menos 2 bilhetes válidos (selecionou {len(bilhetes_aceitos)})")
            return False
        bilhetes_recusados = [b for b in bilhetes_pendentes if b not in bilhetes_aceitos]

        # Adiciona bilhetes aceitos à mão do jogador
        jogador = self.jogo.buscarJogador(jogador_id)
        if not jogador:
            print(f" Jogador {jogador_id} não encontrado")
            return False

        for bilhete in bilhetes_aceitos:
            jogador.bilhetes.append(bilhete)

        # Devolve bilhetes recusados ao FINAL do baralho
        if bilhetes_recusados:
            self.jogo.gerenciadorDeBaralho.devolverBilhetes(bilhetes_recusados)

        # Remove os bilhetes pendentes deste jogador
        del self.jogo.bilhetesPendentesEscolha[jogador_id]

        print(f" Jogador {jogador_id} escolheu {len(bilhetes_aceitos)} bilhetes, recusou {len(bilhetes_recusados)}")
        return True