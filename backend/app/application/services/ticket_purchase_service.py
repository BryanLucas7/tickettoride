"""
TicketPurchaseService - Serviço para compra de bilhetes de destino

GRASP:
- Pure Fabrication: Serviço artificial para coordenar compra de bilhetes
- Information Expert: Delega operações para as entidades corretas
- Low Coupling: Depende apenas de GameActionService e BilheteHelpers
- High Cohesion: Foca exclusivamente na lógica de compra de bilhetes

Refatoração DRY:
- Usa BilheteHelpers para eliminar duplicação com JogoBilhetesService
"""

from typing import Dict, List
from ...core.domain.entities import Jogo, Jogador
from ...core.domain.entities.bilhete_destino import BilheteDestino
from .game_action_service import GameActionService
from ...shared.validators import GameValidators
from ...shared.exception_handlers import handle_validation_errors
from ...core.domain.support.bilhete_helpers import BilheteHelpers


class TicketPurchaseService:
    """
    Serviço responsável pela lógica de compra de bilhetes de destino.
    
    Responsabilidades:
    1. Validar índices de bilhetes escolhidos
    2. Selecionar bilhetes da reserva do jogador
    3. Devolver bilhetes recusados ao baralho
    4. Integrar com GameActionService para passar turno automaticamente
    5. Formatar resposta da compra
    """
    
    def __init__(self, action_service: GameActionService):
        """
        Inicializa o serviço com dependências necessárias.
        
        Args:
            action_service: Serviço para ações de jogo (passar turno, verificar fim)
        """
        self.action_service = action_service
    
    @handle_validation_errors
    def comprar_bilhetes(
        self,
        jogo: Jogo,
        jogador: Jogador,
        indices_escolhidos: List[int]
    ) -> Dict:
        """
        Executa a compra de bilhetes de destino pelo jogador.
        
        Fluxo:
        1. Busca bilhetes reservados para o jogador
        2. Valida índices escolhidos
        3. Seleciona bilhetes aceitos e recusados
        4. Adiciona bilhetes aceitos à mão do jogador
        5. Devolve bilhetes recusados ao baralho
        6. Limpa reserva de bilhetes
        7. Passa turno automaticamente (compra é ação completa)
        
        Args:
            jogo: Instância do jogo
            jogador: Jogador já validado (via Depends(get_validated_player))
            indices_escolhidos: Lista de índices dos bilhetes escolhidos (0, 1, 2...)
        
        Returns:
            Dict com resultado da compra e informações do turno
            
        Raises:
            ValueError: Se não há bilhetes reservados ou índices inválidos
        """
        # 1. Buscar bilhetes reservados
        bilhetes_reservados = self._buscar_bilhetes_reservados(jogo, jogador.id)
        
        # 2. Validar índices usando validador centralizado
        GameValidators.validar_indices(
            indices_escolhidos,
            len(bilhetes_reservados),
            "bilhete",
            minimo=1
        )
        
        # 3. Selecionar bilhetes
        bilhetes_escolhidos, bilhetes_recusados = self._selecionar_bilhetes(
            bilhetes_reservados,
            indices_escolhidos
        )
        
        # 4. Executar compra
        self._executar_compra(
            jogo,
            jogador,
            bilhetes_escolhidos,
            bilhetes_recusados
        )
        
        # 5. Passar turno automaticamente (compra é ação completa)
        resultado_turno = self.action_service.passar_turno_e_verificar_fim(jogo)
        
        # 6. Formatar resposta
        return self._formatar_resposta(
            jogador,
            bilhetes_escolhidos,
            bilhetes_recusados,
            resultado_turno
        )
    
    def _buscar_bilhetes_reservados(self, jogo: Jogo, player_id: str) -> List[BilheteDestino]:
        """
        Busca os bilhetes reservados para o jogador.
        
        Information Expert: Jogo conhece os bilhetes pendentes de compra
        
        Args:
            jogo: Instância do jogo
            player_id: ID do jogador
            
        Returns:
            Lista de bilhetes reservados
            
        Raises:
            ValueError: Se não há bilhetes reservados para o jogador
        """
        bilhetes_reservados = jogo.estado.bilhetes_state.obter_bilhetes_reservados(player_id)
        
        if not bilhetes_reservados:
            raise ValueError(
                f"Não há bilhetes reservados para compra pelo jogador {player_id}. "
                "O jogador deve primeiro visualizar bilhetes disponíveis."
            )
        
        return bilhetes_reservados
    
    def _selecionar_bilhetes(
        self,
        bilhetes_reservados: List[BilheteDestino],
        indices_escolhidos: List[int]
    ) -> tuple[List[BilheteDestino], List[BilheteDestino]]:
        """
        Separa bilhetes em escolhidos e recusados.
        
        Usa BilheteHelpers.separar_bilhetes_por_indices() para eliminar duplicação.
        
        Args:
            bilhetes_reservados: Lista de bilhetes reservados
            indices_escolhidos: Índices dos bilhetes que o jogador quer
            
        Returns:
            Tupla (bilhetes_escolhidos, bilhetes_recusados)
        """
        return BilheteHelpers.separar_bilhetes_por_indices(
            bilhetes_reservados,
            indices_escolhidos
        )
    
    def _executar_compra(
        self,
        jogo: Jogo,
        jogador: Jogador,
        bilhetes_escolhidos: List[BilheteDestino],
        bilhetes_recusados: List[BilheteDestino]
    ) -> None:
        """
        Executa a compra adicionando bilhetes ao jogador e devolvendo recusados.
        
        Usa BilheteHelpers.processar_escolha_bilhetes() para eliminar duplicação
        com JogoBilhetesService.escolherBilhetesIniciais().
        
        Args:
            jogo: Instância do jogo
            jogador: Jogador já validado
            bilhetes_escolhidos: Bilhetes que o jogador ficou
            bilhetes_recusados: Bilhetes que o jogador devolveu
        """
        # Processa escolha usando helper centralizado
        BilheteHelpers.processar_escolha_bilhetes(
            jogador,
            bilhetes_escolhidos,
            bilhetes_recusados,
            jogo.gerenciadorDeBaralhoBilhetes
        )
        
        # Limpar reserva para permitir novas compras futuras
        jogo.estado.bilhetes_state.limpar_bilhetes_reservados(jogador.id)
    
    def _formatar_resposta(
        self,
        jogador: Jogador,
        bilhetes_escolhidos: List[BilheteDestino],
        bilhetes_recusados: List[BilheteDestino],
        resultado_turno: Dict
    ) -> Dict:
        """
        Formata a resposta da compra de bilhetes.
        
        Args:
            jogador: Jogador que fez a compra
            bilhetes_escolhidos: Bilhetes que o jogador ficou
            bilhetes_recusados: Bilhetes que o jogador devolveu
            resultado_turno: Resultado do passar turno (do GameActionService)
            
        Returns:
            Dict com informações formatadas da compra
        """
        from ...shared.response_builder import ResponseBuilder
        from ...shared.message_builder import MessageBuilder
        
        quantidade_escolhidos = len(bilhetes_escolhidos)
        quantidade_recusados = len(bilhetes_recusados)
        
        # Usa MessageBuilder para criar mensagem (migrado de EntityFormatters)
        mensagem = MessageBuilder.criar_mensagem_compra_bilhetes(
            jogador.nome,
            bilhetes_escolhidos,
            quantidade_recusados
        )
        
        return ResponseBuilder.success_with_turn(
            message=mensagem,
            resultado_turno=resultado_turno,
            tickets_kept=quantidade_escolhidos,
            tickets_returned=quantidade_recusados
        )
