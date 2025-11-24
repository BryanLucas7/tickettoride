"""
Service para cálculo de pontuação final do jogo

GRASP Principles:
- Pure Fabrication: Serviço criado para extrair lógica de pontuação final
- High Cohesion: Responsável apenas por cálculo de pontuação final
- Low Coupling: Desacoplado dos routes, pode ser reutilizado
- Controller: Orquestra múltiplos calculators para obter resultado final
"""

from typing import Dict, List, Any, Union
from fastapi import HTTPException

from ...core.domain.entities.jogo import Jogo
from ...core.domain.calculators.pontuacao_final_calculator import PontuacaoFinalCalculator
from ...core.domain.calculators.verificador_bilhetes import VerificadorBilhetes
from .longest_path_service import LongestPathService
from ...shared.formatters import EntityFormatters
from ...constants import BONUS_MAIOR_CAMINHO


class PontuacaoFinalService:
    """
    Serviço responsável por calcular pontuação final do jogo.
    
    Coordena calculators para obter pontuação de cada jogador,
    aplicar bônus, determinar vencedor e formatar resposta.
    """
    
    def __init__(
        self,
        verificador_bilhetes: VerificadorBilhetes = None,
        longest_path_service: LongestPathService = None
    ):
        """
        Inicializa o serviço com seus calculators.
        
        Args:
            verificador_bilhetes: Calculator para verificar bilhetes completos
            longest_path_service: Service para calcular maior caminho
        """
        self.verificador_bilhetes = verificador_bilhetes or VerificadorBilhetes()
        self.longest_path_service = longest_path_service or LongestPathService()
        self.calculator = PontuacaoFinalCalculator(
            verificador_bilhetes=self.verificador_bilhetes,
            longest_path_calculator=self.longest_path_service.calculator
        )
    
    def calcular_resultado_final(self, jogo: Jogo) -> Dict[str, Any]:
        """
        Calcula resultado final do jogo.
        
        Args:
            jogo: Instância do jogo finalizado
            
        Returns:
            Dicionário com:
            - success: bool
            - pontuacoes: Lista de pontuações de cada jogador
            - vencedor: ID do vencedor ou lista de IDs em caso de empate
            - mensagem: Mensagem de resultado
            
        Raises:
            HTTPException: Se jogo não estiver finalizado
        """
        if not jogo.finalizado:
            raise HTTPException(status_code=400, detail="Game not finished yet")
        
        # 1. Calcular pontuações de todos os jogadores
        resultados = self._calcular_pontuacoes_jogadores(jogo)
        
        # 2. Aplicar bônus de maior caminho
        self._aplicar_bonus_maior_caminho(resultados)
        
        # 3. Determinar vencedor(es) com critérios de desempate
        vencedor = self.calculator.determinar_vencedor(resultados)
        
        # 4. Formatar resposta
        return self._formatar_resposta(jogo, resultados, vencedor)
    
    def _calcular_pontuacoes_jogadores(self, jogo: Jogo) -> Dict[str, Any]:
        """
        Calcula pontuação de todos os jogadores.
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            Dicionário com resultados de cada jogador (id -> resultado)
        """
        resultados = {}
        
        for jogador in jogo.gerenciadorDeTurnos.jogadores:
            # Obter rotas conquistadas pelo jogador
            rotas_jogador = jogo.rotas_do_jogador(jogador)
            
            # Calcular pontuação
            resultado = self.calculator.calcular_pontuacao_jogador(
                jogador_id=jogador.id,
                pontos_rotas=jogo.placar.obter_pontuacao(jogador.id) if jogo.placar else 0,
                bilhetes=jogador.bilhetes,
                rotas_conquistadas=rotas_jogador
            )
            
            resultados[jogador.id] = resultado
        
        return resultados
    
    def _aplicar_bonus_maior_caminho(self, resultados: Dict[str, Any]) -> None:
        """
        Aplica bônus de maior caminho para jogador(es) com maior caminho.
        
        Modifica o dicionário de resultados in-place.
        
        Args:
            resultados: Dicionário com resultados de cada jogador
        """
        # Determinar maior comprimento de caminho
        maior_comprimento = max(
            (r.comprimento_maior_caminho for r in resultados.values()),
            default=0
        )
        
        # Aplicar bônus para jogadores com maior caminho
        for resultado in resultados.values():
            if resultado.comprimento_maior_caminho == maior_comprimento and maior_comprimento > 0:
                resultado.bonus_maior_caminho = BONUS_MAIOR_CAMINHO
                resultado.pontuacao_total += BONUS_MAIOR_CAMINHO
            else:
                resultado.bonus_maior_caminho = 0
    

    
    def _formatar_resposta(
        self, 
        jogo: Jogo, 
        resultados: Dict[str, Any], 
        vencedor: Union[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Formata resposta final com todas as informações.
        
        Args:
            jogo: Instância do jogo
            resultados: Dicionário com resultados de cada jogador
            vencedor: ID do vencedor ou lista de IDs em caso de empate
            
        Returns:
            Dicionário formatado para resposta da API
        """
        # Converter resultados para JSON
        pontuacoes = []
        for jogador_id, resultado in resultados.items():
            jogador = jogo.buscarJogador(jogador_id)
            
            pontuacoes.append({
                "jogador_id": jogador_id,
                "jogador_nome": jogador.nome if jogador else f"Jogador {jogador_id}",
                "jogador_cor": jogador.cor.value if jogador else "unknown",
                "pontos_rotas": resultado.pontos_rotas,
                "bilhetes_completos": EntityFormatters.formatar_bilhetes(
                    resultado.bilhetes_completos_lista,
                    completos=[True] * len(resultado.bilhetes_completos_lista),
                    formato="origem_destino"
                ),
                "bilhetes_incompletos": EntityFormatters.formatar_bilhetes(
                    resultado.bilhetes_incompletos_lista,
                    completos=[False] * len(resultado.bilhetes_incompletos_lista),
                    formato="origem_destino"
                ),
                "pontos_bilhetes_positivos": resultado.pontos_bilhetes_completos,
                "pontos_bilhetes_negativos": resultado.pontos_bilhetes_incompletos,
                "bonus_maior_caminho": resultado.bonus_maior_caminho > 0,
                "pontos_maior_caminho": resultado.bonus_maior_caminho,
                "pontuacao_total": resultado.pontuacao_total,
                "tamanho_maior_caminho": resultado.comprimento_maior_caminho
            })
        
        # Ordenar por pontuação (maior primeiro)
        pontuacoes.sort(key=lambda p: p["pontuacao_total"], reverse=True)
        
        # Criar mensagem de vencedor
        mensagem = self._criar_mensagem_vencedor(jogo, vencedor)
        
        return {
            "success": True,
            "pontuacoes": pontuacoes,
            "vencedor": vencedor,
            "mensagem": mensagem
        }
    
    def _criar_mensagem_vencedor(
        self, 
        jogo: Jogo, 
        vencedor: Union[str, List[str]]
    ) -> str:
        """
        Cria mensagem de vencedor.
        
        Args:
            jogo: Instância do jogo
            vencedor: ID do vencedor ou lista de IDs em caso de empate
            
        Returns:
            Mensagem formatada
        """
        if isinstance(vencedor, list):
            nomes = [jogo.buscarJogador(v).nome for v in vencedor]
            return f"Empate! Vencedores: {', '.join(nomes)}"
        else:
            jogador_vencedor = jogo.buscarJogador(vencedor)
            return f"{jogador_vencedor.nome} venceu o jogo!"
