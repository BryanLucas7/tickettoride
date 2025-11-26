"""
Service para ações comuns do jogo (passar turno, verificar fim, etc.)

GRASP: 
- Pure Fabrication: Serviço criado para evitar duplicação de lógica
- Low Coupling: Centraliza lógica de fim de jogo
- High Cohesion: Responsável apenas por ações de turno/fim de jogo
"""

from typing import Dict, Any, Optional, Iterable
from collections import Counter
from ...core.domain.entities.jogo import Jogo
from ...core.domain.entities.rota import Rota
from ...core.domain.entities.jogador import Jogador
from ...core.domain.entities.cor import Cor


class GameActionService:
    """
    Serviço responsável por ações comuns do jogo.
    
    Centraliza lógica de:
    - Passar turno
    - Verificar e processar fim de jogo
    - Resetar estado de compra de cartas
    """
    
    def passar_turno_e_verificar_fim(self, jogo: Jogo) -> Dict[str, Any]:
        """
        Passa o turno e verifica se o jogo terminou (última rodada).
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            Dicionário com:
            - jogo_terminou: bool - Se o jogo terminou
            - mensagem_fim: str|None - Mensagem de fim (se terminou)
            - proximo_jogador: str - ID do próximo jogador
        """
        jogadores = jogo.gerenciadorDeTurnos.jogadores
        total_jogadores = len(jogadores)
        mensagem_fim: Optional[str] = None
        jogo_terminou = False
        proximo_jogador_id: Optional[str] = None

        # Tenta avançar para um jogador que tenha alguma jogada possível.
        for _ in range(total_jogadores):
            jogo.resetar_estado_compra()
            jogo.passar_turno()
            proximo = jogo.gerenciadorDeTurnos.getJogadorAtual()
            proximo_jogador_id = proximo.id if proximo else None

            # Processa fim de jogo por regra oficial (última rodada).
            terminou_oficial, mensagem_oficial = self._processar_fim_oficial(jogo)
            if terminou_oficial:
                jogo_terminou = True
                mensagem_fim = mensagem_oficial
                break

            # Autopass: se jogador não tem nenhuma jogada possível, continue para o próximo.
            if proximo and not self._jogador_tem_jogada_possivel(jogo, proximo):
                continue

            # Encontrou jogador com jogada possível, encerra loop.
            break
        else:
            # Nenhum jogador com jogada possível -> fim de jogo por deadlock.
            jogo.acoes.encerrar()
            jogo_terminou = True
            mensagem_fim = "Jogo encerrado: nenhum jogador tem jogadas possíveis."
            proximo_jogador_id = None

        # Checagem global de deadlock mesmo após selecionar próximo
        if not jogo_terminou and self._nenhum_jogador_tem_jogada(jogo):
            jogo.acoes.encerrar()
            jogo_terminou = True
            mensagem_fim = "Jogo encerrado: nenhum jogador tem jogadas possíveis."
            proximo_jogador_id = None

        return {
            "jogo_terminou": jogo_terminou,
            "mensagem_fim": mensagem_fim,
            "proximo_jogador": proximo_jogador_id
        }
    
    def formatar_resposta_com_fim_turno(
        self, 
        jogo: Jogo, 
        response_base: Dict[str, Any], 
        passar_turno: bool = True
    ) -> Dict[str, Any]:
        """
        Formata resposta de uma ação do jogo com informações de fim de turno.
        
        Este método centraliza a lógica de adicionar informações de turno
        e fim de jogo às respostas, evitando duplicação em múltiplos services.
        
        Args:
            jogo: Instância do jogo
            response_base: Dicionário base com a resposta da ação
            passar_turno: Se True, passa o turno automaticamente
            
        Returns:
            Dicionário response_base atualizado com:
            - turn_completed: bool - Se o turno foi completado
            - turno_passado: bool - Se o turno foi passado
            - next_player: str|None - ID do próximo jogador (se turno passado)
            - jogo_terminou: bool|None - Se o jogo terminou (se turno passado)
            - mensagem_fim: str|None - Mensagem de fim (se jogo terminou)
            
        Example:
            >>> response = {"success": True, "message": "Carta comprada"}
            >>> service.formatar_resposta_com_fim_turno(jogo, response)
            {
                "success": True,
                "message": "Carta comprada",
                "turn_completed": True,
                "turno_passado": True,
                "next_player": "player_2",
                "jogo_terminou": False,
                "mensagem_fim": None
            }
        """
        turno_completo = jogo.estado.estado_compra.turnoCompleto if hasattr(jogo, 'estado') and hasattr(jogo.estado, 'estado_compra') else passar_turno
        
        response_base["turn_completed"] = turno_completo
        
        if passar_turno and turno_completo:
            resultado_turno = self.passar_turno_e_verificar_fim(jogo)
            response_base.update({
                "turno_passado": True,
                "next_player": resultado_turno["proximo_jogador"],
                "jogo_terminou": resultado_turno["jogo_terminou"],
                "mensagem_fim": resultado_turno["mensagem_fim"]
            })
        else:
            response_base["turno_passado"] = False
        
        return response_base

    # ============================================================
    # Regras de jogada possível (USA)
    # ============================================================
    def _jogador_tem_jogada_possivel(self, jogo: Jogo, jogador: Jogador) -> bool:
        """Retorna True se o jogador pode fazer ao menos uma ação (rota, comprar carta, comprar bilhete)."""
        return (
            self._pode_reivindicar_alguma_rota(jogo, jogador)
            or self._pode_comprar_cartas(jogo)
            or self._pode_comprar_bilhetes(jogo)
        )

    def _pode_reivindicar_alguma_rota(self, jogo: Jogo, jogador: Jogador) -> bool:
        """Verifica se existe ao menos uma rota que o jogador possa reivindicar."""
        if not jogo.tabuleiro or not jogo.tabuleiro.rotas:
            return False

        for rota in jogo.tabuleiro.rotas:
            if not self._rota_disponivel(jogo, rota, jogador):
                continue
            if len(jogador.vagoes) < rota.comprimento:
                continue
            if self._tem_cartas_para_rota(jogador, rota):
                return True
        return False

    def _rota_disponivel(self, jogo: Jogo, rota: Rota, jogador: Jogador) -> bool:
        """Aplica regras de bloqueio de rota e rotas duplas."""
        if rota.proprietario is not None:
            return False

        total_jogadores = len(jogo.gerenciadorDeTurnos.jogadores)
        for dupla in getattr(jogo, "rotasDuplas", []) or []:
            if rota.id not in dupla:
                continue
            outra_id = dupla[0] if dupla[1] == rota.id else dupla[1]
            outra_rota = jogo.tabuleiro.obterRotaPorId(outra_id)

            if total_jogadores <= 3:
                # Em 2-3 jogadores, apenas uma das rotas duplas pode ser usada na partida.
                if outra_rota and outra_rota.proprietario is not None:
                    return False
            else:
                # Em 4-5 jogadores, mesma pessoa não pode pegar as duas.
                if outra_rota and outra_rota.proprietario == jogador:
                    return False

        return True

    def _tem_cartas_para_rota(self, jogador: Jogador, rota: Rota) -> bool:
        """Verifica se o jogador possui combinação de cartas válida para a rota."""
        cartas = getattr(jogador, "cartasVagao", []) or []
        locos = sum(1 for c in cartas if getattr(c, "ehLocomotiva", False) or getattr(c, "cor", None) == Cor.LOCOMOTIVA)
        counts = Counter()

        for c in cartas:
            if getattr(c, "ehLocomotiva", False):
                continue
            cor_val = getattr(c, "cor", None)
            if hasattr(cor_val, "value"):
                cor_val = cor_val.value
            if cor_val:
                counts[cor_val] += 1

        necessario = rota.comprimento
        cor_rota = getattr(rota, "cor", None)
        cor_rota_val = cor_rota.value if hasattr(cor_rota, "value") else cor_rota

        if cor_rota in (None, Cor.CINZA):
            # Rota cinza: escolher uma única cor + locomotivas
            for cor, qtd in counts.items():
                if qtd + locos >= necessario:
                    return True
            return locos >= necessario

        return counts.get(cor_rota_val, 0) + locos >= necessario

    def _pode_comprar_cartas(self, jogo: Jogo) -> bool:
        """Verifica se existe ao menos uma carta de trem disponível (baralho, descarte, abertas)."""
        baralho = getattr(getattr(jogo, "gerenciadorDeBaralhoVagoes", None), "baralhoVagoes", None)
        descarte = getattr(getattr(jogo, "gerenciadorDeBaralhoVagoes", None), "descarteVagoes", []) or []
        abertas = getattr(getattr(jogo, "gerenciadorDeBaralhoVagoes", None), "cartasAbertas", []) or []

        cartas_baralho = len(baralho.cartas) if baralho else 0
        if cartas_baralho > 0:
            return True
        if abertas:
            return True
        if descarte:
            return True
        return False

    def _pode_comprar_bilhetes(self, jogo: Jogo) -> bool:
        """Verifica se há bilhetes disponíveis para compra."""
        ger_bilhetes = getattr(jogo, "gerenciadorDeBaralhoBilhetes", None)
        if ger_bilhetes and getattr(ger_bilhetes, "quantidade_restante", 0) > 0:
            return True
        return False

    def _nenhum_jogador_tem_jogada(self, jogo: Jogo) -> bool:
        """Retorna True se nenhum jogador tiver jogadas possíveis."""
        for jogador in jogo.gerenciadorDeTurnos.jogadores:
            if self._jogador_tem_jogada_possivel(jogo, jogador):
                return False
        return True

    def _processar_fim_oficial(self, jogo: Jogo) -> tuple[bool, Optional[str]]:
        """Processa regra oficial de fim de jogo (última rodada)."""
        if jogo.estado.gerenciador_fim and jogo.estado.gerenciador_fim.ultima_rodada_ativada:
            resultado_fim = jogo.estado.gerenciador_fim.processar_turno_jogado()
            if resultado_fim["jogo_terminou"]:
                jogo.acoes.encerrar()
                return True, resultado_fim["mensagem"]
        return False, None

    def autopassar_se_necessario(self, jogo: Jogo) -> Optional[Dict[str, Any]]:
        """
        Se o jogador atual não tiver jogadas possíveis, passa o turno automaticamente.
        Retorna resultado de passar_turno_e_verificar_fim se autopassar for executado.
        """
        jogador_atual = jogo.gerenciadorDeTurnos.getJogadorAtual()

        # Deadlock global: encerra
        if self._nenhum_jogador_tem_jogada(jogo):
            jogo.acoes.encerrar()
            return {
                "jogo_terminou": True,
                "mensagem_fim": "Jogo encerrado: nenhum jogador tem jogadas possíveis.",
                "proximo_jogador": None
            }

        if jogador_atual and not self._jogador_tem_jogada_possivel(jogo, jogador_atual):
            return self.passar_turno_e_verificar_fim(jogo)

        return None
