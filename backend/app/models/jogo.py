from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .gerenciador_de_turnos import GerenciadorDeTurnos
from .gerenciador_de_baralho import GerenciadorDeBaralho
from .placar import Placar
from .tabuleiro import Tabuleiro
from .bilhete_destino import BilheteDestino
from .estado_compra_cartas import EstadoCompraCartas
from .descarte_manager import DescarteManager
from .validador_rotas_duplas import ValidadorRotasDuplas
from .gerenciador_fim_jogo import GerenciadorFimDeJogo
from .pathfinder import VerificadorBilhetes

try:
    from ..data.mapa_brasil import carregar_tabuleiro_brasil
except ImportError:  # Suporte para execuções fora do pacote "app"
    from data.mapa_brasil import carregar_tabuleiro_brasil

@dataclass
class Jogo:
    id: int
    gerenciadorDeTurnos: GerenciadorDeTurnos = field(default_factory=GerenciadorDeTurnos)
    gerenciadorDeBaralho: Optional[GerenciadorDeBaralho] = None
    placar: Optional[Placar] = None
    tabuleiro: Tabuleiro = field(default_factory=Tabuleiro) #esta classe é necessaria visto ter o mapaBrasil.ts?d
    iniciado: bool = False
    finalizado: bool = False
    rotasDuplas: List[Tuple[str, str]] = field(default_factory=list)
    descarteManager: Optional[DescarteManager] = None
    gerenciadorFimDeJogo: GerenciadorFimDeJogo = field(default_factory=GerenciadorFimDeJogo)
    pathfinder: Optional[VerificadorBilhetes] = None  # Verificador de bilhetes completados
    # Armazena os bilhetes pendentes de escolha inicial para cada jogador
    bilhetesPendentesEscolha: Dict[str, List[BilheteDestino]] = field(default_factory=dict)
    # Armazena bilhetes sorteados aguardando confirmação de compra durante a partida
    bilhetesPendentesCompra: Dict[str, List[BilheteDestino]] = field(default_factory=dict)
    # Estado de compra de cartas do turno atual
    estadoCompraCartas: EstadoCompraCartas = field(default_factory=EstadoCompraCartas)

    def buscarJogador(self, jogador_id: str):
        """Retorna o jogador com o ID informado ou None."""
        return next(
            (j for j in self.gerenciadorDeTurnos.jogadores if str(j.id) == str(jogador_id)),
            None,
        )

    def iniciar(self):
        """Inicializa o jogo
        
        Aplica princípios GRASP:
        - Controller: Jogo coordena a inicialização
        - Information Expert: GerenciadorDeBaralho possui as cartas
        """
        self._configurar_tabuleiro_padrao()

        # Inicializa componentes
        self.placar = Placar(jogadores=self.gerenciadorDeTurnos.jogadores)
        self.gerenciadorDeBaralho = GerenciadorDeBaralho()
        self.descarteManager = DescarteManager(
            pilha_descarte=self.gerenciadorDeBaralho.descarteVagoes
        )
        self.gerenciadorFimDeJogo.resetar()
        self.gerenciadorFimDeJogo.total_jogadores = len(self.gerenciadorDeTurnos.jogadores)
        self.pathfinder = VerificadorBilhetes()  # Inicializa verificador de bilhetes
        
        # Distribui 4 cartas iniciais para cada jogador (regra oficial)
        self._distribuirCartasIniciais()
        
        # Distribui 3 bilhetes de destino para escolha inicial
        self._distribuirBilhetesIniciais()

        if self.tabuleiro.validador_duplas:
            self.tabuleiro.validador_duplas.numero_jogadores = len(self.gerenciadorDeTurnos.jogadores)
        
        self.iniciado = True

    def _configurar_tabuleiro_padrao(self):
        """Popula o tabuleiro com o mapa brasileiro padrão."""

        info = carregar_tabuleiro_brasil(self.tabuleiro)
        rotas_duplas = info.get("rotas_duplas", []) if isinstance(info, dict) else []
        self.rotasDuplas = list(rotas_duplas)

        if rotas_duplas:
            validador = ValidadorRotasDuplas(
                numero_jogadores=len(self.gerenciadorDeTurnos.jogadores)
            )
            for rota_id_a, rota_id_b in rotas_duplas:
                rota_a = self.tabuleiro.obterRotaPorId(rota_id_a)
                rota_b = self.tabuleiro.obterRotaPorId(rota_id_b)
                if rota_a and rota_b:
                    validador.registrar_rota_dupla(rota_a, rota_b)
            self.tabuleiro.validador_duplas = validador
    
    def _distribuirCartasIniciais(self):
        """Distribui 4 cartas de vagão para cada jogador
        
        Regra oficial: Cada jogador começa com 4 cartas de vagão
        """
        for jogador in self.gerenciadorDeTurnos.jogadores:
            for _ in range(4):
                carta = self.gerenciadorDeBaralho.comprarCartaVagaoViewer(visivel=False)
                if carta:
                    jogador.comprarCartaVagao(carta)
        
        print(f"[OK] Distribuidas 4 cartas iniciais para {len(self.gerenciadorDeTurnos.jogadores)} jogadores")

    def _distribuirBilhetesIniciais(self):
        """Distribui 3 bilhetes de destino para escolha inicial de cada jogador
        
        Regra oficial: Cada jogador recebe 3 bilhetes e DEVE ficar com pelo menos 2
        Os bilhetes recusados são devolvidos ao FINAL do baralho
        """
        for jogador in self.gerenciadorDeTurnos.jogadores:
            bilhetes = self.gerenciadorDeBaralho.comprarBilhetes()
            # Armazena os bilhetes pendentes de escolha para este jogador
            self.bilhetesPendentesEscolha[jogador.id] = bilhetes
        
        print(f" Distribuídos 3 bilhetes iniciais para {len(self.gerenciadorDeTurnos.jogadores)} jogadores (aguardando escolha)")

    def escolherBilhetesIniciais(self, jogador_id: str, bilhetes_escolhidos_ids: List[object]) -> bool:
        """Processa a escolha de bilhetes iniciais de um jogador
        
        Args:
            jogador_id: ID do jogador (UUID string)
            bilhetes_escolhidos_ids: IDs dos bilhetes que o jogador deseja FICAR (mínimo 2)
            
        Returns:
            True se a escolha foi válida e processada
        """
        # Verifica se o jogador tem bilhetes pendentes
        if jogador_id not in self.bilhetesPendentesEscolha:
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
        
        bilhetes_pendentes = self.bilhetesPendentesEscolha[jogador_id]

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
        jogador = self.buscarJogador(jogador_id)
        if not jogador:
            print(f" Jogador {jogador_id} não encontrado")
            return False
        
        for bilhete in bilhetes_aceitos:
            jogador.bilhetes.append(bilhete)
        
        # Devolve bilhetes recusados ao FINAL do baralho
        if bilhetes_recusados:
            self.gerenciadorDeBaralho.devolverBilhetes(bilhetes_recusados)
        
        # Remove os bilhetes pendentes deste jogador
        del self.bilhetesPendentesEscolha[jogador_id]
        
        print(f" Jogador {jogador_id} escolheu {len(bilhetes_aceitos)} bilhetes, recusou {len(bilhetes_recusados)}")
        return True

    def comprarCartaDoBaralhoFechado(self, jogador_id: int) -> dict:
        """Compra uma carta do baralho fechado
        
        Args:
            jogador_id: ID do jogador que está comprando
            
        Returns:
            Dict com sucesso, carta comprada e mensagem
            
        Aplica GRASP Controller: Jogo coordena a ação de compra
        """
        # Verifica se pode comprar do fechado
        if not self.estadoCompraCartas.podeComprarCartaFechada():
            return {
                "sucesso": False,
                "mensagem": self.estadoCompraCartas.obterMensagemStatus()
            }
        
        # Busca jogador
        jogador = next((j for j in self.gerenciadorDeTurnos.jogadores if j.id == jogador_id), None)
        if not jogador:
            return {"sucesso": False, "mensagem": f"Jogador {jogador_id} não encontrado"}
        
        # Compra carta do baralho
        carta = self.gerenciadorDeBaralho.comprarCartaVagaoViewer(visivel=False)
        
        if not carta:
            return {"sucesso": False, "mensagem": "Baralho vazio"}
        
        # Adiciona carta ao jogador
        jogador.comprarCartaVagao(carta)
        
        # Registra compra no estado
        self.estadoCompraCartas.registrarCompraCartaFechada()
        
        return {
            "sucesso": True,
            "carta": {"cor": carta.cor.value, "ehLocomotiva": carta.ehLocomotiva},
            "cartasCompradas": self.estadoCompraCartas.cartasCompradas,
            "turnoCompleto": self.estadoCompraCartas.turnoCompleto,
            "mensagem": self.estadoCompraCartas.obterMensagemStatus()
        }

    def comprarCartaAberta(self, jogador_id: int, indice: int) -> dict:
        """Compra uma carta das 5 cartas abertas
        
        Args:
            jogador_id: ID do jogador que está comprando
            indice: Índice da carta aberta (0-4)
            
        Returns:
            Dict com sucesso, carta comprada e mensagem
            
        Aplica GRASP Controller: Jogo coordena a ação de compra
        Aplica GRASP Information Expert: GerenciadorDeBaralho valida e executa compra
        """
        # Busca jogador
        jogador = next((j for j in self.gerenciadorDeTurnos.jogadores if j.id == jogador_id), None)
        if not jogador:
            return {"sucesso": False, "mensagem": f"Jogador {jogador_id} não encontrado"}
        
        # Verifica índice válido
        if indice < 0 or indice >= 5:
            return {"sucesso": False, "mensagem": f"Índice inválido: {indice}"}
        
        # Obtém informação da carta antes de comprar
        cartas_abertas = self.gerenciadorDeBaralho.obterCartasAbertas()
        if indice >= len(cartas_abertas):
            return {"sucesso": False, "mensagem": "Carta não disponível"}
        
        carta_desejada = cartas_abertas[indice]
        
        # Verifica se pode comprar esta carta (regras de locomotiva)
        if not self.estadoCompraCartas.podeComprarCartaAberta(ehLocomotiva=carta_desejada.ehLocomotiva):
            return {
                "sucesso": False,
                "mensagem": self.estadoCompraCartas.obterMensagemStatus()
            }
        
        # Compra carta aberta (repõe automaticamente)
        carta = self.gerenciadorDeBaralho.comprarCartaVagaoVisivel(indice)
        
        if not carta:
            return {"sucesso": False, "mensagem": "Erro ao comprar carta"}
        
        # Adiciona carta ao jogador
        jogador.comprarCartaVagao(carta)
        
        # Registra compra no estado
        self.estadoCompraCartas.registrarCompraCartaAberta(ehLocomotiva=carta.ehLocomotiva)
        
        return {
            "sucesso": True,
            "carta": {"cor": carta.cor.value, "ehLocomotiva": carta.ehLocomotiva},
            "cartasCompradas": self.estadoCompraCartas.cartasCompradas,
            "turnoCompleto": self.estadoCompraCartas.turnoCompleto,
            "cartasAbertas": [{"cor": c.cor.value, "ehLocomotiva": c.ehLocomotiva} for c in self.gerenciadorDeBaralho.obterCartasAbertas()],
            "mensagem": self.estadoCompraCartas.obterMensagemStatus()
        }

    def obterEstadoCompra(self) -> dict:
        """Retorna o estado atual de compra de cartas
        
        Returns:
            Dict com informações do estado de compra
        """
        return {
            "cartasCompradas": self.estadoCompraCartas.cartasCompradas,
            "comprouLocomotivaDasAbertas": self.estadoCompraCartas.comprouLocomotivaDasAbertas,
            "turnoCompleto": self.estadoCompraCartas.turnoCompleto,
            "podeComprarFechada": self.estadoCompraCartas.podeComprarCartaFechada(),
            "cartasAbertas": [{"cor": c.cor.value, "ehLocomotiva": c.ehLocomotiva} for c in self.gerenciadorDeBaralho.obterCartasAbertas()] if self.gerenciadorDeBaralho else [],
            "mensagem": self.estadoCompraCartas.obterMensagemStatus()
        }

    def proximar(self):
        """Avança para o próximo turno
        
        Reseta o estado de compra para o novo turno
        """
        # Reseta estado de compra de cartas
        self.estadoCompraCartas.resetar()
        
        return self.gerenciadorDeTurnos.proximoJogador()

    def jogar(self, acao: str, parametros: dict = None):
        """Executa uma ação de jogo
        
        Args:
            acao: Tipo de ação (comprar_carta, reivindicar_rota, etc)
            parametros: Parâmetros específicos da ação
        """
        jogador_atual = self.gerenciadorDeTurnos.getJogadorAtual()
        
        if acao == "comprar_carta":
            carta = self.gerenciadorDeBaralho.comprarCartaVagaoViewer()
            if carta:
                jogador_atual.comprarCartaVagao(carta)
        
        elif acao == "reivindicar_rota":
            if parametros and "rota_id" in parametros:
                rota = self.tabuleiro.obterRotaPorId(parametros["rota_id"])
                if rota and parametros.get("cartas"):
                    if rota.reivindicarRota(jogador_atual, parametros["cartas"]):
                        jogador_atual.reivindicarRota(rota)
                        # Adiciona pontos baseado no comprimento da rota
                        pontos_rota = {1: 1, 2: 2, 3: 4, 4: 7, 5: 10, 6: 15}
                        jogador_atual.pontuacao += pontos_rota.get(rota.comprimento, 0)
        
        elif acao == "comprar_bilhetes":
            bilhetes = self.gerenciadorDeBaralho.comprarBilhetes()
            aceitos = jogador_atual.comprarBilhetesDestino(bilhetes)
            nao_aceitos = [b for b in bilhetes if b not in aceitos]
            self.gerenciadorDeBaralho.devolverBilhetes(nao_aceitos)
        
        elif acao == "passar":
            jogador_atual.passarTurno()

    def validarFimDeJogo(self) -> bool:
        """Valida se o jogo chegou ao fim
        
        Returns:
            True se o jogo deve terminar
        """
        # Fim de jogo quando qualquer jogador tiver 2 ou menos vagões
        for jogador in self.gerenciadorDeTurnos.jogadores:
            if len(jogador.vagoes) <= 2:
                return True
        return False

    def encerrar(self):
        """Encerra o jogo"""
        self.finalizado = True
        if self.placar:
            self.placar.atualizarPlacar()
