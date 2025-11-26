"""
Tipos e contratos do domínio.

Define TypedDicts e tipos para garantir contratos explícitos
entre camadas da aplicação.

Padrão GRASP: Protected Variations
- Contratos explícitos protegem contra mudanças de estrutura
- Se a estrutura mudar, o tipo checker avisa todos os lugares afetados
"""

from typing import TypedDict, Optional


class ResultadoTurno(TypedDict):
    """
    Contrato para resultado de passagem de turno.
    
    Usado por:
    - GameActionService.passar_turno_e_verificar_fim()
    - ResponseBuilder.success_with_turn()
    - Services que precisam passar turno automaticamente
    
    Garante tipagem explícita e evita erros de chave inexistente.
    """
    proximo_jogador: str
    jogo_terminou: bool
    mensagem_fim: Optional[str]


class ResultadoCompra(TypedDict, total=False):
    """
    Contrato para resultado de compra de cartas.
    
    total=False permite campos opcionais.
    """
    success: bool
    message: str
    carta: dict
    cartasCompradas: int
    turnoCompleto: bool
    cartasAbertas: list


class ResultadoConquista(TypedDict, total=False):
    """
    Contrato para resultado de conquista de rota.
    """
    success: bool
    message: str
    pontos_ganhos: int
    trens_restantes: int
    fim_de_jogo_ativado: bool
    cartas_descartadas: int
    trens_removidos: int
