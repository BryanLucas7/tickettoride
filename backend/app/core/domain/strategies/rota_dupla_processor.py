"""
Processador de Conquistas de Rotas Duplas.

Padrão GRASP: Pure Fabrication
Princípio SRP: Responsável APENAS por processar conquistas e bloquear rotas.

Modifica estado - executa a conquista e bloqueia rotas paralelas.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.rota import Rota
    from ..entities.jogador import Jogador

from ..support.responses import success_response, error_response
from .rota_dupla_validator import RotaDuplaValidator


@dataclass
class RotaDuplaProcessor:
    """
    Responsável por processar conquistas e bloquear rotas paralelas.
    
    SRP: Este processor modifica estado, ao contrário do validator.
    
    Responsabilidades:
    1. Validar conquista (delegando para validator)
    2. Atribuir rota ao jogador
    3. Bloquear rota paralela em jogos 2-3 jogadores
    """
    
    validator: RotaDuplaValidator
    
    def processar_conquista(self, rota: 'Rota', jogador: 'Jogador') -> dict:
        """Processa conquista de rota e bloqueia paralela se necessário.
        
        Args:
            rota: Rota sendo conquistada
            jogador: Jogador conquistando
            
        Returns:
            dict com resultado do processamento:
            - success: bool
            - message: str
            - bloqueou_paralela: bool
            - rota_bloqueada_id: str (opcional)
        """
        validacao = self.validator.validar_conquista(rota, jogador)
        
        if not validacao["valido"]:
            return error_response(validacao["mensagem"], bloqueou_paralela=False)
        
        self._executar_conquista(rota, jogador)
        bloqueou, rota_bloqueada_id = self._bloquear_paralela_se_necessario(rota)
        mensagem = self._construir_mensagem(jogador, bloqueou, rota_bloqueada_id)
        
        return success_response(
            mensagem, 
            bloqueou_paralela=bloqueou, 
            rota_bloqueada_id=rota_bloqueada_id
        )
    
    def _executar_conquista(self, rota: 'Rota', jogador: 'Jogador') -> None:
        """Atribui a rota ao jogador."""
        rota.proprietario = jogador
        rota.ehConcluida = True
    
    def _bloquear_paralela_se_necessario(self, rota: 'Rota') -> tuple:
        """Bloqueia rota paralela em jogos 2-3 jogadores.
        
        Returns:
            Tupla (bloqueou: bool, rota_bloqueada_id: str | None)
        """
        if self.validator.numero_jogadores >= 4:
            return False, None
        
        dupla = self.validator.encontrar_rota_dupla(rota)
        if not dupla:
            return False, None
        
        bloqueou = self._bloquear_rota_paralela(dupla)
        if not bloqueou:
            return False, None
        
        rota_bloqueada_id = self._obter_id_rota_bloqueada(dupla)
        return True, rota_bloqueada_id
    
    def _bloquear_rota_paralela(self, dupla) -> bool:
        """Executa o bloqueio da rota paralela."""
        if dupla.rota1.proprietario and not dupla.rota2.proprietario:
            dupla.rota2.proprietario = "BLOQUEADO"
            return True
        elif dupla.rota2.proprietario and not dupla.rota1.proprietario:
            dupla.rota1.proprietario = "BLOQUEADO"
            return True
        return False
    
    def _obter_id_rota_bloqueada(self, dupla) -> str:
        """Obtém o ID da rota que foi bloqueada."""
        if dupla.rota1.proprietario == "BLOQUEADO":
            return dupla.rota1.id
        elif dupla.rota2.proprietario == "BLOQUEADO":
            return dupla.rota2.id
        return None
    
    def _construir_mensagem(self, jogador: 'Jogador', bloqueou: bool, rota_id: str) -> str:
        """Constrói mensagem de sucesso."""
        nome = jogador.nome if hasattr(jogador, 'nome') else jogador
        mensagem = f"Rota conquistada por {nome}"
        if bloqueou:
            mensagem += f" (rota paralela bloqueada: {rota_id})"
        return mensagem
