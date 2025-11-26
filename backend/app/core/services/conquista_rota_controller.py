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
from typing import List, Dict
from ..domain.entities.jogador import Jogador
from ..domain.entities.rota import Rota
from ..domain.entities.carta_vagao import CartaVagao
from ..domain.strategies.rota_dupla_validator import RotaDuplaValidator
from ..domain.calculators.calculadora_pontos_rota import CalculadoraPontosRota
from .conquista_rota_validator import ConquistaRotaValidator
from .conquista_rota_processor import ConquistaRotaProcessor
from .conquista_rota_result_builder import ConquistaRotaResultBuilder, DadosConquista
from ..domain.support.responses import normalize_result


@dataclass
class ConquistaRotaController:
    """
    Controller - Coordena ação completa de conquistar rota.
    
    Responsabilidades:
    - Coordenar componentes especializados
    - Orquestrar fluxo de conquista
    - Retornar resultado final
    
    GRASP Principles:
    - Controller: Coordena fluxo complexo
    - Indirection: Separa cliente da lógica
    - Low Coupling: Delega para componentes especializados
    """
    
    validator: ConquistaRotaValidator = field(default_factory=ConquistaRotaValidator)
    processor: ConquistaRotaProcessor = field(default_factory=ConquistaRotaProcessor)
    result_builder: ConquistaRotaResultBuilder = field(default_factory=ConquistaRotaResultBuilder)
    
    def conquistar_rota(
        self,
        jogador: Jogador,
        rota: Rota,
        cartas_usadas: List[CartaVagao],
        total_jogadores: int,
        validador_duplas: RotaDuplaValidator = None
    ) -> Dict:
        """
        Processa conquista completa de rota.
        
        Args:
            jogador: Jogador que está conquistando
            rota: Rota a ser conquistada
            cartas_usadas: Lista de cartas que o jogador usará
            total_jogadores: Total de jogadores no jogo
            validador_duplas: Validador de rotas duplas (opcional)
            
        Returns:
            Dicionário com resultado detalhado
        """
        # 1. Configurar dependências nos componentes
        self.validator = ConquistaRotaValidator(validador_duplas)
        self.processor = ConquistaRotaProcessor()
        
        # 2. Validar conquista
        resultado_validacao = self.validator.validar_conquista(jogador, rota, cartas_usadas)
        resultado_val_norm = normalize_result(resultado_validacao)
        if not resultado_val_norm['success']:
            return self.result_builder.construir_resultado_erro(resultado_val_norm['message'])
        
        # 3. Processar conquista física
        resultado_processamento = self.processor.processar_conquista(
            jogador, rota, cartas_usadas, validador_duplas, total_jogadores
        )
        resultado_proc_norm = normalize_result(resultado_processamento)
        if not resultado_proc_norm['success']:
            return self.result_builder.construir_resultado_erro(resultado_proc_norm['message'])
        
        # 4. Calcular pontos (separado do builder - SRP)
        pontos = CalculadoraPontosRota.calcular_pontos(rota.comprimento)
        
        # 5. Construir dados para o result builder
        dados = DadosConquista(
            pontos=pontos,
            cartas_descartadas=resultado_processamento['resultado_conquista']['cartas_descartadas'],
            trens_removidos=resultado_processamento['resultado_conquista']['trens_removidos'],
            trens_restantes=resultado_processamento['resultado_conquista']['trens_restantes'],
            rota_dupla_bloqueada=resultado_processamento['rota_dupla_bloqueada']
        )
        
        # 6. Construir resultado final
        return self.result_builder.construir_resultado_sucesso(
            jogador=jogador,
            rota=rota,
            dados=dados
        )
