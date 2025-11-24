"""
Response Assembler - Montador centralizado de respostas compostas

Padrão GRASP: Pure Fabrication
- Centraliza responsabilidade de compor respostas complexas que agregam múltiplas entidades
- Reduz duplicação de código de montagem de respostas em endpoints e serviços
- Facilita manutenção e garante consistência de formato
- Segue convenções: snake_case, campos obrigatórios padronizados

Refatoração DRY Checklist #4: Formatação centralizada de entidades
"""

from typing import Dict, Any, Optional
from ..core.domain.entities.jogo import Jogo
from ..core.domain.entities.jogador import Jogador
from .formatters import EntityFormatters


class ResponseAssembler:
    """
    Classe utilitária para montagem de respostas compostas da API.
    
    Combina EntityFormatters para criar respostas complexas que agregam
    múltiplas entidades do domínio (jogadores + cartas + rotas, etc).
    """
    
    @staticmethod
    def montar_estado_jogo_completo(jogo: Jogo, jogador_atual_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Monta estado completo do jogo para resposta da API.
        
        Agrega: jogadores, cartas visíveis, status do jogo.
        
        Args:
            jogo: Instância do jogo
            jogador_atual_id: ID do jogador atual (opcional, usa gerenciador se None)
            
        Returns:
            Dict com estado completo do jogo
            
        Example:
            >>> estado = ResponseAssembler.montar_estado_jogo_completo(jogo)
            >>> estado.keys()
            dict_keys(['game_id', 'iniciado', 'finalizado', 'jogadores', 'jogador_atual_id', 'cartas_visiveis'])
        """
        # Determinar jogador atual
        if jogador_atual_id is None and jogo.iniciado:
            jogador_atual = jogo.gerenciadorDeTurnos.getJogadorAtual()
            jogador_atual_id = jogador_atual.id if jogador_atual else None
        
        # Formatar jogadores com informações básicas
        jogadores_formatados = []
        for jogador in jogo.gerenciadorDeTurnos.jogadores:
            jogador_info = EntityFormatters.formatar_jogador(
                jogador, 
                incluir_cartas=False, 
                incluir_bilhetes=False
            )
            # Adicionar pontos do placar se disponível
            if jogo.placar:
                jogador_info["pontos"] = jogo.placar.obter_pontuacao(jogador.id)
            jogadores_formatados.append(jogador_info)
        
        # Formatar cartas visíveis
        cartas_visiveis = []
        cartas_fechadas_restantes = 0
        if jogo.gerenciadorDeBaralho:
            cartas_visiveis = EntityFormatters.formatar_cartas(
                jogo.gerenciadorDeBaralho.cartasAbertas
            )
            cartas_fechadas_restantes = len(jogo.gerenciadorDeBaralho.baralhoVagoes.cartas)
        
        cartas_fechadas_disponiveis = cartas_fechadas_restantes  # apenas baralho fechado

        return {
            "game_id": jogo.id,
            "iniciado": jogo.iniciado,
            "finalizado": jogo.finalizado,
            "jogadores": jogadores_formatados,
            "jogador_atual_id": jogador_atual_id,
            "cartas_visiveis": cartas_visiveis,
            "cartas_fechadas_restantes": cartas_fechadas_restantes,
            "cartas_fechadas_disponiveis": cartas_fechadas_disponiveis,
            "pode_comprar_carta_fechada": cartas_fechadas_disponiveis > 0
        }
    
    @staticmethod
    def montar_painel_rotas(jogo: Jogo, incluir_proprietario_detalhes: bool = True) -> Dict[str, Any]:
        """
        Monta painel de rotas do tabuleiro.
        
        Args:
            jogo: Instância do jogo
            incluir_proprietario_detalhes: Se deve incluir nome e cor do proprietário
            
        Returns:
            Dict com lista de rotas formatadas
            
        Example:
            >>> painel = ResponseAssembler.montar_painel_rotas(jogo)
            >>> painel.keys()
            dict_keys(['game_id', 'total_rotas', 'rotas_livres', 'rotas_conquistadas', 'rotas'])
        """
        rotas_formatadas = []
        rotas_livres = 0
        rotas_conquistadas = 0
        
        for rota in jogo.tabuleiro.rotas:
            rota_info = EntityFormatters.formatar_rota(rota)
            
            # Adicionar detalhes do proprietário se solicitado
            if incluir_proprietario_detalhes and rota.proprietario:
                rota_info["proprietario_nome"] = rota.proprietario.nome
                rota_info["proprietario_cor"] = rota.proprietario.cor.value
            
            rotas_formatadas.append(rota_info)
            
            if rota.proprietario:
                rotas_conquistadas += 1
            else:
                rotas_livres += 1
        
        return {
            "game_id": jogo.id,
            "total_rotas": len(jogo.tabuleiro.rotas),
            "rotas_livres": rotas_livres,
            "rotas_conquistadas": rotas_conquistadas,
            "rotas": rotas_formatadas
        }
    
    @staticmethod
    def montar_mao_jogador(
        jogo: Jogo, 
        jogador: Jogador, 
        incluir_bilhetes: bool = True,
        incluir_cartas: bool = True,
        verificar_bilhetes_completos: bool = True
    ) -> Dict[str, Any]:
        """
        Monta informações completas da mão de um jogador.
        
        Args:
            jogo: Instância do jogo
            jogador: Instância do jogador
            incluir_bilhetes: Se deve incluir bilhetes
            incluir_cartas: Se deve incluir cartas
            verificar_bilhetes_completos: Se deve verificar bilhetes completos com pathfinder
            
        Returns:
            Dict com cartas, bilhetes e estatísticas do jogador
            
        Example:
            >>> mao = ResponseAssembler.montar_mao_jogador(jogo, jogador)
            >>> mao.keys()
            dict_keys(['player_id', 'nome', 'cor', 'cartas', 'bilhetes', 'num_cartas', 'num_bilhetes', 'trens_restantes', 'pontos'])
        """
        resposta = {
            "player_id": jogador.id,
            "nome": jogador.nome,
            "cor": jogador.cor.value,
            "num_cartas": len(jogador.cartasVagao),
            "num_bilhetes": len(jogador.bilhetes),
            "trens_restantes": len(jogador.vagoes),  # Número de vagões disponíveis
            "pontos": jogo.placar.obter_pontuacao(jogador.id) if jogo.placar else 0
        }
        
        # Incluir cartas se solicitado
        if incluir_cartas:
            resposta["cartas"] = EntityFormatters.formatar_cartas(jogador.cartasVagao)
        
        # Incluir bilhetes se solicitado
        if incluir_bilhetes:
            if verificar_bilhetes_completos and jogo.pathfinder:
                # Obter rotas conquistadas pelo jogador
                rotas_jogador = jogo.rotas_do_jogador(jogador)
                
                # Verificar quais bilhetes foram completados
                completos_status = []
                for bilhete in jogador.bilhetes:
                    completo = jogo.pathfinder.verificar_bilhete_completo(
                        bilhete=bilhete,
                        rotas_conquistadas=rotas_jogador
                    )
                    completos_status.append(completo)
                
                resposta["bilhetes"] = EntityFormatters.formatar_bilhetes(
                    jogador.bilhetes, 
                    completos=completos_status
                )
            else:
                # Sem verificação de completude
                resposta["bilhetes"] = EntityFormatters.formatar_bilhetes(jogador.bilhetes)
        
        return resposta
    
    @staticmethod
    @staticmethod
    def montar_criacao_jogo(jogo: Jogo, incluir_jogadores_detalhados: bool = True) -> Dict[str, Any]:
        """
        Monta resposta de criação de jogo.
        
        Args:
            jogo: Instância do jogo recém-criado
            incluir_jogadores_detalhados: Se deve incluir detalhes completos dos jogadores
            
        Returns:
            Dict com informações do jogo criado
            
        Example:
            >>> resposta = ResponseAssembler.montar_criacao_jogo(jogo)
            >>> resposta.keys()
            dict_keys(['game_id', 'numero_jogadores', 'iniciado', 'finalizado', 'jogadores'])
        """
        if incluir_jogadores_detalhados:
            jogadores_info = [
                {
                    "id": j.id,
                    "nome": j.nome,
                    "cor": j.cor.value,
                    "trens_disponiveis": len(j.vagoes),  # Número de vagões disponíveis
                    "num_cartas": len(j.cartasVagao)
                }
                for j in jogo.gerenciadorDeTurnos.jogadores
            ]
        else:
            jogadores_info = [
                {
                    "id": j.id,
                    "nome": j.nome,
                    "cor": j.cor.value
                }
                for j in jogo.gerenciadorDeTurnos.jogadores
            ]
        
        return {
            "game_id": jogo.id,
            "numero_jogadores": len(jogo.gerenciadorDeTurnos.jogadores),
            "iniciado": jogo.iniciado,
            "finalizado": jogo.finalizado,
            "jogadores": jogadores_info
        }
