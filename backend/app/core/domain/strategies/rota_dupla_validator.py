"""
Validador de Rotas Duplas.

Padrão GRASP: Pure Fabrication
Princípio SRP: Responsável APENAS por validação de rotas duplas.

Não modifica estado - apenas verifica se conquistas são válidas.
"""

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.rota import Rota
    from ..entities.jogador import Jogador

from ..entities.rota_dupla import RotaDupla


@dataclass
class RotaDuplaValidator:
    """
    Responsável APENAS por validação de rotas duplas.
    
    SRP: Este validador não modifica estado, apenas verifica 
    se uma conquista é válida segundo as regras de rotas duplas.
    
    Regras:
    1. Um jogador não pode conquistar ambas rotas de um par
    2. Em jogos 2-3 jogadores, só uma rota do par pode ser conquistada
    """
    
    rotas_duplas: List[RotaDupla] = field(default_factory=list)
    numero_jogadores: int = 4
    
    def encontrar_rota_dupla(self, rota: 'Rota') -> Optional[RotaDupla]:
        """Encontra a dupla que contém esta rota.
        
        Args:
            rota: Rota a procurar
            
        Returns:
            RotaDupla que contém a rota, ou None
        """
        for dupla in self.rotas_duplas:
            if dupla.contem_rota(rota):
                return dupla
        return None
    
    def validar_conquista(self, rota: 'Rota', jogador: 'Jogador' = None) -> dict:
        """Valida se rota pode ser conquistada (regra de rotas duplas).
        
        Args:
            rota: Rota que jogador quer conquistar
            jogador: Jogador que está tentando conquistar
            
        Returns:
            dict com resultado da validação:
            - valido: bool
            - mensagem: str
            - rota_bloqueada: bool
            - rota_paralela_id: str (opcional)
        """
        resultado_basico = self._validar_rota_disponivel(rota)
        if not resultado_basico["valido"]:
            return resultado_basico
        
        dupla = self.encontrar_rota_dupla(rota)
        if not dupla:
            return {"valido": True, "mensagem": "Rota válida (não é dupla)", "rota_bloqueada": False}
        
        resultado_jogador = self._validar_mesmo_jogador(dupla, rota, jogador)
        if not resultado_jogador["valido"]:
            return resultado_jogador
        
        resultado_poucos_jogadores = self._validar_regra_poucos_jogadores(dupla)
        if not resultado_poucos_jogadores["valido"]:
            return resultado_poucos_jogadores
        
        return {"valido": True, "mensagem": "Rota válida", "rota_bloqueada": False}
    
    def _validar_rota_disponivel(self, rota: 'Rota') -> dict:
        """Verifica se a rota está disponível para conquista."""
        if not rota.proprietario:
            return {"valido": True, "mensagem": "", "rota_bloqueada": False}
        
        if rota.proprietario == "BLOQUEADO":
            return {
                "valido": False,
                "mensagem": "Rota bloqueada: rota paralela já foi conquistada",
                "rota_bloqueada": True
            }
        
        nome = rota.proprietario.nome if hasattr(rota.proprietario, 'nome') else rota.proprietario
        return {
            "valido": False,
            "mensagem": f"Rota já conquistada por {nome}",
            "rota_bloqueada": False
        }
    
    def _validar_mesmo_jogador(self, dupla: RotaDupla, rota: 'Rota', jogador: 'Jogador') -> dict:
        """Valida regra universal: mesmo jogador não pode conquistar ambas rotas."""
        if not jogador:
            return {"valido": True, "mensagem": "", "rota_bloqueada": False}
        
        rota_paralela = dupla.obter_rota_paralela(rota)
        if not rota_paralela or not rota_paralela.proprietario:
            return {"valido": True, "mensagem": "", "rota_bloqueada": False}
        
        if rota_paralela.proprietario == "BLOQUEADO":
            return {"valido": True, "mensagem": "", "rota_bloqueada": False}
        
        if not (hasattr(rota_paralela.proprietario, 'id') and hasattr(jogador, 'id')):
            return {"valido": True, "mensagem": "", "rota_bloqueada": False}
        
        if rota_paralela.proprietario.id == jogador.id:
            return {
                "valido": False,
                "mensagem": (
                    f"❌ Você já conquistou a rota paralela "
                    f"{rota_paralela.cidadeA.nome} → {rota_paralela.cidadeB.nome}. "
                    "Um jogador não pode conquistar ambas rotas duplas!"
                ),
                "rota_bloqueada": True,
                "rota_paralela_id": rota_paralela.id
            }
        
        return {"valido": True, "mensagem": "", "rota_bloqueada": False}
    
    def _validar_regra_poucos_jogadores(self, dupla: RotaDupla) -> dict:
        """Valida regra de 2-3 jogadores: só uma rota do par pode ser conquistada."""
        if self.numero_jogadores >= 4:
            return {"valido": True, "mensagem": "", "rota_bloqueada": False}
        
        rota_conquistada = dupla.obter_rota_conquistada()
        if rota_conquistada:
            return {
                "valido": False,
                "mensagem": "Rota bloqueada: rota paralela já conquistada (regra 2-3 jogadores)",
                "rota_bloqueada": True,
                "rota_paralela_id": rota_conquistada.id
            }
        
        return {"valido": True, "mensagem": "", "rota_bloqueada": False}
