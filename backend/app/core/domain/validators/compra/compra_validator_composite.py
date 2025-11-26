"""
CompraValidator - Composite que coordena validadores de compra.

GoF Pattern: Composite
- Agrupa validadores específicos (JogadorValidator, CartaFechadaValidator, etc)
- Mantém API compatível com código existente
- Delega para validators especializados

GRASP: Pure Fabrication
- Classe artificial criada para coordenar validações

Refatoração: Esta classe substitui o CompraValidator original,
mantendo a mesma API pública para não quebrar código existente.
"""

from typing import Tuple, Optional, TYPE_CHECKING

from .jogador_validator import JogadorValidator, JogadorValidationResult
from .carta_fechada_validator import CartaFechadaValidator, CompraFechadaValidationResult
from .carta_aberta_validator import CartaAbertaValidator, CompraAbertaValidationResult

if TYPE_CHECKING:
    from ...entities.carta_vagao import CartaVagao
    from ...entities.jogador import Jogador


class CompraValidationResult:
    """
    Resultado de uma validação de compra.
    
    Mantém compatibilidade com código existente.
    """
    
    def __init__(
        self, 
        valido: bool, 
        erro: Optional[str] = None, 
        jogador: Optional['Jogador'] = None
    ):
        self.valido = valido
        self.erro = erro
        self.jogador = jogador
    
    @property
    def invalido(self) -> bool:
        """Conveniência para verificar se é inválido."""
        return not self.valido
    
    @classmethod
    def from_jogador_result(cls, result: JogadorValidationResult) -> 'CompraValidationResult':
        """Converte JogadorValidationResult para CompraValidationResult."""
        return cls(
            valido=result.valido,
            erro=result.erro,
            jogador=result.jogador
        )
    
    @classmethod
    def from_fechada_result(cls, result: CompraFechadaValidationResult) -> 'CompraValidationResult':
        """Converte CompraFechadaValidationResult para CompraValidationResult."""
        return cls(valido=result.valido, erro=result.erro)
    
    @classmethod
    def from_aberta_result(cls, result: CompraAbertaValidationResult) -> 'CompraValidationResult':
        """Converte CompraAbertaValidationResult para CompraValidationResult."""
        return cls(valido=result.valido, erro=result.erro)


class CompraValidator:
    """
    Composite que coordena validadores de compra.
    
    Refatoração SRP: Delega para validators específicos:
    - JogadorValidator: valida existência de jogador
    - CartaFechadaValidator: valida compra do baralho
    - CartaAbertaValidator: valida compra das cartas abertas
    
    Mantém API compatível com CompraValidator original.
    
    Exemplo de uso (mesma API anterior):
        validator = CompraValidator(jogo)
        resultado = validator.validar_compra_carta_fechada_completa(jogador_id)
        if resultado.invalido:
            return error_response(resultado.erro)
    """
    
    def __init__(self, jogo):
        """
        Inicializa o composite com referência ao jogo.
        
        Cria instâncias dos validators específicos internamente.
        
        Args:
            jogo: Instância do jogo para acessar estado e componentes
        """
        self.jogo = jogo
        
        # Instancia validators específicos (Composite Pattern)
        self._jogador_validator = JogadorValidator(jogo.gerenciadorDeTurnos)
        self._carta_fechada_validator = CartaFechadaValidator(
            jogo.estado.estado_compra,
            jogo.gerenciadorDeBaralhoVagoes
        )
        self._carta_aberta_validator = CartaAbertaValidator(
            jogo.estado.estado_compra,
            jogo.gerenciadorDeBaralhoVagoes
        )
    
    # === API Pública (compatibilidade com código existente) ===
    
    def validar_jogador(self, jogador_id: str) -> CompraValidationResult:
        """
        Valida se jogador existe no jogo.
        
        DELEGADO para JogadorValidator.
        """
        resultado = self._jogador_validator.validar(jogador_id)
        return CompraValidationResult.from_jogador_result(resultado)
    
    def validar_compra_fechada(self) -> CompraValidationResult:
        """
        Valida se compra de carta fechada é permitida.
        
        DELEGADO para CartaFechadaValidator.
        
        Refatoração SRP: Lógica movida para CartaFechadaValidator._validar_estado_compra().
        Composite agora apenas delega.
        """
        resultado = self._carta_fechada_validator._validar_estado_compra()
        return CompraValidationResult.from_fechada_result(resultado)
    
    def validar_indice_carta_aberta(self, indice: int) -> CompraValidationResult:
        """
        Valida se índice da carta aberta é válido.
        
        DELEGADO para CartaAbertaValidator._validar_indice().
        """
        resultado = self._carta_aberta_validator._validar_indice(indice)
        return CompraValidationResult.from_aberta_result(resultado)
    
    def validar_compra_aberta(self, carta: 'CartaVagao') -> CompraValidationResult:
        """
        Valida se compra de carta aberta específica é permitida.
        
        DELEGADO para CartaAbertaValidator.
        
        Refatoração SRP: Lógica movida para CartaAbertaValidator._validar_regras_compra().
        Composite agora apenas delega.
        
        Args:
            carta: Carta que o jogador quer comprar
        """
        resultado = self._carta_aberta_validator._validar_regras_compra(carta)
        return CompraValidationResult.from_aberta_result(resultado)
    
    def validar_baralho_disponivel(self) -> CompraValidationResult:
        """
        Valida se há cartas disponíveis no baralho.
        
        DELEGADO para CartaFechadaValidator._validar_disponibilidade().
        """
        resultado = self._carta_fechada_validator._validar_disponibilidade()
        return CompraValidationResult.from_fechada_result(resultado)
    
    def validar_compra_carta_fechada_completa(
        self, 
        jogador_id: str
    ) -> CompraValidationResult:
        """
        Validação completa para compra de carta fechada.
        
        Combina validações usando validators específicos:
        1. Validar estado de compra (CartaFechadaValidator)
        2. Validar jogador (JogadorValidator)
        
        Args:
            jogador_id: ID do jogador
            
        Returns:
            CompraValidationResult com jogador se todas validações passarem
        """
        # 1. Validar estado de compra
        resultado_estado = self.validar_compra_fechada()
        if resultado_estado.invalido:
            return resultado_estado
        
        # 2. Validar jogador
        resultado_jogador = self.validar_jogador(jogador_id)
        if resultado_jogador.invalido:
            return resultado_jogador
        
        return resultado_jogador
    
    def validar_compra_carta_aberta_completa(
        self, 
        jogador_id: str, 
        indice: int
    ) -> Tuple[CompraValidationResult, Optional['CartaVagao']]:
        """
        Validação completa para compra de carta aberta.
        
        Combina validações:
        1. Validar jogador (JogadorValidator)
        2. Validar índice e regras (CartaAbertaValidator)
        
        Args:
            jogador_id: ID do jogador
            indice: Índice da carta (0-4)
            
        Returns:
            Tupla (CompraValidationResult, carta_desejada)
        """
        # 1. Validar jogador
        resultado_jogador = self._jogador_validator.validar(jogador_id)
        if resultado_jogador.invalido:
            return (CompraValidationResult.from_jogador_result(resultado_jogador), None)
        
        # 2. Validar carta aberta (índice + regras)
        resultado_carta = self._carta_aberta_validator.validar(indice)
        if resultado_carta.invalido:
            return (CompraValidationResult.from_aberta_result(resultado_carta), None)
        
        # Retornar com jogador do primeiro resultado
        return (
            CompraValidationResult(valido=True, jogador=resultado_jogador.jogador),
            resultado_carta.carta
        )
    
    def ha_opcao_de_compra(self) -> bool:
        """
        Verifica se existe alguma carta que possa ser comprada neste turno.
        
        DELEGADO para validators específicos.
        
        Refatoração SRP: Coordena validators especializados ao invés de
        implementar lógica diretamente.
        
        Returns:
            True se há pelo menos uma carta disponível para compra
        """
        estado = self.jogo.estado.estado_compra

        if estado.turnoCompleto:
            return False

        # Delega verificação de carta fechada para CartaFechadaValidator
        if self._carta_fechada_validator.pode_comprar():
            return True

        # Delega verificação de cartas abertas para CartaAbertaValidator
        return self._carta_aberta_validator.tem_carta_compravel()
