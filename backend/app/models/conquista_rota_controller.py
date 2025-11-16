"""
PADRÃO GRASP: Controller
- ConquistaRotaController coordena toda a ação de conquistar rota
- Integra todas as validações e operações

PADRÃO GRASP: Indirection
- API separa UI da lógica de negócio
- Cliente não precisa conhecer detalhes de implementação

PADRÃO GRASP: Low Coupling
- Componentes separados: validação, descarte, pontuação, regras duplas
- Cada componente focado em sua responsabilidade

Fluxo Completo de Conquista de Rota:
1. Validar se rota está disponível
2. Validar se jogador tem cartas corretas (Strategy Pattern)
3. Validar regra de rotas duplas (2-3 jogadores)
4. Remover cartas da mão do jogador
5. Descartar cartas usadas
6. Remover trens do jogador
7. Marcar rota como conquistada
8. Calcular e adicionar pontos (Observer Pattern)
9. Notificar observers de pontuação
10. Verificar fim de jogo (≤2 trens)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .jogador import Jogador
from .rota import Rota
from .carta_vagao import CartaVagao
from .descarte_manager import DescarteManager, ConquistaRotaService
from .rota_validation_strategy import criar_estrategia_validacao
from .validador_rotas_duplas import ValidadorRotasDuplas
from .placar import Placar
from .gerenciador_fim_jogo import GerenciadorFimDeJogo


@dataclass
class ConquistaRotaController:
    """
    Controller - Coordena ação completa de conquistar rota.
    
    Responsabilidades:
    - Coordenar todas as validações
    - Processar conquista de rota
    - Integrar todos os componentes
    - Retornar resultado detalhado
    
    GRASP Principles:
    - Controller: Coordena fluxo complexo
    - Indirection: Separa cliente da lógica
    - Low Coupling: Usa componentes especializados
    """
    
    descarte_manager: DescarteManager = field(default_factory=DescarteManager)
    validador_duplas: Optional[ValidadorRotasDuplas] = None
    placar: Optional[Placar] = None
    gerenciador_fim_jogo: Optional[GerenciadorFimDeJogo] = None
    
    def conquistar_rota(
        self,
        jogador: Jogador,
        rota: Rota,
        cartas_usadas: List[CartaVagao],
        total_jogadores: int
    ) -> Dict:
        """
        Processa conquista completa de rota.
        
        Args:
            jogador: Jogador que está conquistando
            rota: Rota a ser conquistada
            cartas_usadas: Lista de cartas que o jogador usará
            total_jogadores: Total de jogadores no jogo (para regra de duplas)
            
        Returns:
            Dicionário com resultado detalhado:
            {
                "sucesso": bool,
                "mensagem": str,
                "pontos_ganhos": int,
                "cartas_descartadas": int,
                "trens_removidos": int,
                "trens_restantes": int,
                "rota_dupla_bloqueada": bool,
                "fim_de_jogo_ativado": bool,
                "detalhes": dict
            }
        """
        # 1. Validar disponibilidade da rota
        if rota.proprietario is not None:
            return self._erro("❌ Rota já foi conquistada por outro jogador!")
        
        # 2. Validar cartas (Strategy Pattern)
        estrategia = criar_estrategia_validacao(rota.cor)
        resultado_validacao = estrategia.validar(
            cartas_jogador=cartas_usadas,
            comprimento=rota.comprimento,
            cor_rota=rota.cor
        )
        
        if not resultado_validacao['valido']:
            return self._erro(f"❌ Cartas inválidas: {resultado_validacao['mensagem']}")
        
        # 3. Validar regra de rotas duplas (aplica-se a TODOS os jogos 2-5 jogadores)
        rota_dupla_bloqueada = False
        if self.validador_duplas:
            resultado_dupla = self.validador_duplas.validar_conquista_rota(rota=rota, jogador=jogador)
            
            if not resultado_dupla['valido']:
                return self._erro(f"❌ {resultado_dupla['mensagem']}")
        
        # 4-6. Processar conquista (descarte, trens, etc)
        resultado_conquista = ConquistaRotaService.conquistar_rota(
            jogador=jogador,
            rota=rota,
            cartas_usadas=cartas_usadas,
            descarte_manager=self.descarte_manager
        )
        
        if not resultado_conquista["sucesso"]:
            return self._erro(resultado_conquista["mensagem"])
        
        # 7. Processar rota dupla e marcar rota como conquistada (se aplicável)
        if self.validador_duplas and total_jogadores <= 3:
            resultado_bloqueio = self.validador_duplas.processar_conquista(rota, jogador)
            rota_dupla_bloqueada = resultado_bloqueio.get('bloqueou_paralela', False)
        else:
            # Se não tem validador duplas, marca manualmente
            rota.reivindicarRota(jogador, cartas_usadas)
        
        # 8. Calcular pontos (tabela de pontuação)
        pontos = self._calcular_pontos_rota(rota.comprimento)
        
        # 9. Adicionar pontos ao jogador (Observer Pattern)
        if self.placar:
            self.placar.adicionar_pontos_rota(
                jogador_id=jogador.id,
                comprimento_rota=rota.comprimento,
                nome_rota=f"{rota.cidadeA.nome} → {rota.cidadeB.nome}"
            )
        
        # 10. Verificar fim de jogo (≤2 trens)
        fim_de_jogo_ativado = False
        alerta_fim = None
        
        if self.gerenciador_fim_jogo:
            trens_restantes = resultado_conquista["trens_restantes"]
            estado_fim = self.gerenciador_fim_jogo.verificar_condicao_fim(
                jogador_id=jogador.id,
                trens_restantes=trens_restantes
            )
            
            fim_de_jogo_ativado = estado_fim.get("fim_ativado", False)
            alerta_fim = estado_fim.get("mensagem")
        
        # 12. Montar resposta de sucesso
        mensagem = self._construir_mensagem_sucesso(
            rota=rota,
            pontos=pontos,
            cartas_descartadas=resultado_conquista["cartas_descartadas"],
            trens_removidos=resultado_conquista["trens_removidos"],
            trens_restantes=resultado_conquista["trens_restantes"],
            fim_de_jogo_ativado=fim_de_jogo_ativado,
            alerta_fim=alerta_fim
        )
        
        return {
            "sucesso": True,
            "mensagem": mensagem,
            "pontos_ganhos": pontos,
            "cartas_descartadas": resultado_conquista["cartas_descartadas"],
            "trens_removidos": resultado_conquista["trens_removidos"],
            "trens_restantes": resultado_conquista["trens_restantes"],
            "rota_dupla_bloqueada": rota_dupla_bloqueada,
            "fim_de_jogo_ativado": fim_de_jogo_ativado,
            "alerta_fim_jogo": alerta_fim,
            "detalhes": {
                "rota_id": rota.id,
                "cidadeA": rota.cidadeA.nome,
                "cidadeB": rota.cidadeB.nome,
                "cor": rota.cor.value,
                "comprimento": rota.comprimento,
                "jogador_id": jogador.id,
                "jogador_nome": jogador.nome
            }
        }
    
    def _erro(self, mensagem: str) -> Dict:
        """Retorna dicionário de erro padronizado"""
        return {
            "sucesso": False,
            "mensagem": mensagem,
            "pontos_ganhos": 0,
            "cartas_descartadas": 0,
            "trens_removidos": 0,
            "trens_restantes": 0,
            "rota_dupla_bloqueada": False,
            "fim_de_jogo_ativado": False,
            "alerta_fim_jogo": None,
            "detalhes": {}
        }
    
    def _calcular_pontos_rota(self, comprimento: int) -> int:
        """
        Calcula pontos conforme tabela de pontuação.
        
        Tabela Ticket to Ride:
        - 1 vagão: 1 ponto
        - 2 vagões: 2 pontos
        - 3 vagões: 4 pontos
        - 4 vagões: 7 pontos
        - 5 vagões: 10 pontos
        - 6 vagões: 15 pontos
        """
        tabela_pontos = {
            1: 1,
            2: 2,
            3: 4,
            4: 7,
            5: 10,
            6: 15
        }
        
        return tabela_pontos.get(comprimento, 0)
    
    def _construir_mensagem_sucesso(
        self,
        rota: Rota,
        pontos: int,
        cartas_descartadas: int,
        trens_removidos: int,
        trens_restantes: int,
        fim_de_jogo_ativado: bool,
        alerta_fim: Optional[str]
    ) -> str:
        """Constrói mensagem de sucesso detalhada"""
        mensagem_base = (
            f"✅ Rota conquistada!\n"
            f"   📍 {rota.cidadeA.nome} → {rota.cidadeB.nome}\n"
            f"   🎯 +{pontos} pontos\n"
            f"   🎴 {cartas_descartadas} cartas descartadas\n"
            f"   🚂 {trens_removidos} trens removidos ({trens_restantes} restantes)"
        )
        
        if fim_de_jogo_ativado and alerta_fim:
            mensagem_base += f"\n\n{alerta_fim}"
        
        return mensagem_base


@dataclass
class ConquistaRotaPreview:
    """
    Serviço para preview de conquista (antes de confirmar).
    
    Útil para UI mostrar informações antes do jogador confirmar.
    """
    
    @staticmethod
    def calcular_preview(
        rota: Rota,
        cartas_disponiveis: List[CartaVagao],
        trens_disponiveis: int
    ) -> Dict:
        """
        Calcula preview de conquista de rota.
        
        Args:
            rota: Rota a ser conquistada
            cartas_disponiveis: Cartas disponíveis na mão do jogador
            trens_disponiveis: Trens disponíveis do jogador
            
        Returns:
            Dicionário com:
            - pode_conquistar: bool
            - cartas_necessarias: int
            - trens_necessarios: int
            - pontos_potenciais: int
            - opcoes_cartas: List de combinações válidas
            - mensagem: str explicativa
        """
        comprimento = rota.comprimento
        pontos = ConquistaRotaController._calcular_pontos_rota(None, comprimento)
        
        # Verificar trens
        pode_por_trens = trens_disponiveis >= comprimento
        
        # Verificar cartas (simplificado - apenas contar por cor)
        estrategia = criar_estrategia_validacao(rota.cor)
        
        # Tentar validar com cartas disponíveis
        resultado_validacao = estrategia.validar(
            cartas_jogador=cartas_disponiveis[:comprimento],
            comprimento=comprimento,
            cor_rota=rota.cor
        )
        
        pode_conquistar = pode_por_trens and resultado_validacao['valido']
        
        mensagem = ""
        if not pode_por_trens:
            mensagem = f"❌ Trens insuficientes (tem {trens_disponiveis}, precisa {comprimento})"
        elif len(cartas_disponiveis) < comprimento:
            mensagem = f"❌ Cartas insuficientes (tem {len(cartas_disponiveis)}, precisa {comprimento})"
        else:
            mensagem = f"✅ Pode conquistar! {comprimento} cartas, {comprimento} trens → +{pontos} pontos"
        
        return {
            "pode_conquistar": pode_conquistar,
            "cartas_necessarias": comprimento,
            "trens_necessarios": comprimento,
            "pontos_potenciais": pontos,
            "mensagem": mensagem,
            "detalhes": {
                "rota_id": rota.id,
                "cidadeA": rota.cidadeA.nome,
                "cidadeB": rota.cidadeB.nome,
                "cor": rota.cor.value,
                "comprimento": comprimento
            }
        }
