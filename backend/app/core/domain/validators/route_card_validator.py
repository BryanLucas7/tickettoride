"""
Validador de cartas para conquista de rotas.

SRP: Responsável APENAS por validar se as cartas são compatíveis com a rota.
Extraído de RouteConquestService para melhorar separação de responsabilidades.

Padrão GRASP: Pure Fabrication
- Classe criada para extrair responsabilidade de validação

REFATORAÇÃO DRY: Agora delega para as Strategies (RotaColoridaStrategy e 
RotaCinzaStrategy) ao invés de duplicar lógica de validação.
"""

from typing import List, Optional
from dataclasses import dataclass

from ..entities.rota import Rota
from ..entities.carta_vagao import CartaVagao
from ..strategies.rota_validation_factory import criar_estrategia_validacao


@dataclass
class CardValidationResult:
    """
    Resultado da validação de cartas.
    
    Attributes:
        valido: Se as cartas são válidas para a rota
        erro: Mensagem de erro (se inválido)
        cartas_validadas: Cartas validadas (se válido)
    """
    valido: bool
    erro: Optional[str] = None
    cartas_validadas: Optional[List[CartaVagao]] = None
    
    @property
    def invalido(self) -> bool:
        """Conveniência para verificar se é inválido."""
        return not self.valido


class RouteCardValidator:
    """
    Valida se cartas são compatíveis com uma rota.
    
    SRP: Única responsabilidade - validar compatibilidade cartas ↔ rota.
    
    REFATORAÇÃO DRY: Delega para Strategies existentes ao invés de duplicar
    lógica de validação de cores. Isso garante que:
    - Regras de negócio ficam em um único lugar (Strategies)
    - Alterações nas regras são propagadas automaticamente
    - Testes das Strategies cobrem também este validador
    
    Regras de validação (delegadas para Strategies):
    - Quantidade de cartas == comprimento da rota
    - Cores compatíveis (mesma cor ou locomotivas)
    - Rotas cinzas aceitam qualquer cor (desde que todas iguais)
    
    Exemplo de uso:
        validator = RouteCardValidator()
        resultado = validator.validar(rota, cartas)
        if resultado.invalido:
            raise HTTPException(status_code=400, detail=resultado.erro)
    """
    
    def validar(
        self, 
        rota: Rota, 
        cartas: List[CartaVagao]
    ) -> CardValidationResult:
        """
        Valida cartas para conquista de rota.
        
        Delega validação de cores para Strategies (DRY).
        
        Args:
            rota: Rota a ser conquistada
            cartas: Cartas que o jogador quer usar
            
        Returns:
            CardValidationResult com status e detalhes
        """
        # Validar quantidade primeiro (rápido, evita processamento desnecessário)
        if len(cartas) != rota.comprimento:
            return CardValidationResult(
                valido=False,
                erro=f"Selecione exatamente {rota.comprimento} carta(s) para conquistar esta rota."
            )
        
        # Delegar validação de cores para Strategy apropriada (DRY)
        estrategia = criar_estrategia_validacao(rota.cor)
        resultado_strategy = estrategia.validar(
            cartas_jogador=cartas,
            comprimento=rota.comprimento,
            cor_rota=rota.cor
        )
        
        if not resultado_strategy['valido']:
            return CardValidationResult(
                valido=False,
                erro=resultado_strategy['mensagem']
            )
        
        return CardValidationResult(
            valido=True,
            cartas_validadas=cartas
        )
