"""

Implementa validação de rotas duplas para jogos com 2-3 jogadores.

Regra: Em jogos de 2-3 jogadores, apenas UMA das rotas duplas pode ser 
conquistada. Quando primeira rota dupla for conquistada, a segunda fica bloqueada.

GRASP Principles Applied:
- Information Expert: Tabuleiro conhece rotas duplas e rotas conquistadas
- Controller: Validador coordena verificação de regras
- Protected Variations: Lógica de rotas duplas encapsulada

Design Decisions:
- Rotas duplas identificadas por mesmas cidades de origem/destino
- Validação baseada em número de jogadores (2-3 vs 4-5)
- Bloqueio automático da rota paralela ao conquistar primeira
"""

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from ..support.responses import success_response, error_response

if TYPE_CHECKING:
    from ..entities.rota import Rota
    from ..entities.jogador import Jogador


@dataclass
class RotaDupla:
    """
    Representa um par de rotas paralelas entre duas cidades.
    
    GRASP Information Expert: Conhece as duas rotas paralelas
    """
    
    rota1: 'Rota'
    rota2: 'Rota'
    
    def obter_rota_disponivel(self) -> Optional['Rota']:
        """Retorna rota disponível (não conquistada)
        
        Returns:
            Rota disponível ou None se ambas conquistadas/bloqueadas
        """
        if not self.rota1.proprietario:
            return self.rota1
        if not self.rota2.proprietario:
            return self.rota2
        return None
    
    def obter_rota_conquistada(self) -> Optional['Rota']:
        """Retorna rota já conquistada
        
        Returns:
            Rota conquistada ou None se nenhuma foi conquistada
        """
        if self.rota1.proprietario:
            return self.rota1
        if self.rota2.proprietario:
            return self.rota2
        return None
    
    def bloquear_paralela(self) -> bool:
        """Bloqueia rota paralela à que foi conquistada
        
        Usado em jogos 2-3 jogadores para impedir conquista de ambas rotas.
        Marca a rota paralela como "bloqueada" (proprietario especial).
        
        Returns:
            True se bloqueou rota paralela, False se já estava bloqueada/conquistada
        """
        if self.rota1.proprietario and not self.rota2.proprietario:
            # Marca rota2 como bloqueada (proprietario = "BLOQUEADO")
            self.rota2.proprietario = "BLOQUEADO"
            return True
        elif self.rota2.proprietario and not self.rota1.proprietario:
            # Marca rota1 como bloqueada
            self.rota1.proprietario = "BLOQUEADO"
            return True
        return False


@dataclass
class ValidadorRotasDuplas:
    """
    Valida e gerencia regra de rotas duplas.
    
    GRASP Controller: Coordena validação de rotas duplas
    GRASP Information Expert: Conhece regras de rotas duplas
    """
    
    rotas_duplas: List[RotaDupla] = field(default_factory=list)
    numero_jogadores: int = 4
    
    def registrar_rota_dupla(self, rota1: 'Rota', rota2: 'Rota'):
        """Registra um par de rotas duplas
        
        Args:
            rota1: Primeira rota do par
            rota2: Segunda rota do par (mesmas cidades)
        """
        dupla = RotaDupla(rota1=rota1, rota2=rota2)
        self.rotas_duplas.append(dupla)
    
    def _encontrar_rota_dupla(self, rota: 'Rota') -> Optional[RotaDupla]:
        """Encontra a dupla que contém esta rota
        
        Args:
            rota: Rota a procurar
            
        Returns:
            RotaDupla que contém a rota, ou None
        """
        for dupla in self.rotas_duplas:
            if dupla.rota1.id == rota.id or dupla.rota2.id == rota.id:
                return dupla
        return None
    
    def validar_conquista_rota(self, rota: 'Rota', jogador: 'Jogador' = None) -> dict:
        """Valida se rota pode ser conquistada (regra de rotas duplas)
        
        Args:
            rota: Rota que jogador quer conquistar
            jogador: Jogador que está tentando conquistar (opcional para validação completa)
            
        Returns:
            dict com resultado: {
                "valido": bool,
                "mensagem": str,
                "rota_bloqueada": bool,
                "rota_paralela_id": str (opcional)
            }
        """
        # Verifica se rota já está conquistada
        if rota.proprietario:
            if rota.proprietario == "BLOQUEADO":
                return {
                    "valido": False,
                    "mensagem": "Rota bloqueada: rota paralela já foi conquistada",
                    "rota_bloqueada": True
                }
            else:
                return {
                    "valido": False,
                    "mensagem": f"Rota já conquistada por {rota.proprietario.nome if hasattr(rota.proprietario, 'nome') else rota.proprietario}",
                    "rota_bloqueada": False
                }
        
        # Verifica se é rota dupla
        dupla = self._encontrar_rota_dupla(rota)
        
        if not dupla:
            # Rota simples, sempre válida
            return {
                "valido": True,
                "mensagem": "Rota válida (não é dupla)",
                "rota_bloqueada": False
            }
        
        # Identifica qual é a rota paralela
        rota_paralela = dupla.rota2 if dupla.rota1.id == rota.id else dupla.rota1
        
        # REGRA UNIVERSAL: Mesmo jogador NÃO pode conquistar ambas rotas duplas
        # (Aplica-se a jogos com 2-5 jogadores)
        if jogador and rota_paralela.proprietario:
            # Verifica se a rota paralela pertence ao mesmo jogador
            if rota_paralela.proprietario != "BLOQUEADO":
                if hasattr(rota_paralela.proprietario, 'id') and hasattr(jogador, 'id'):
                    if rota_paralela.proprietario.id == jogador.id:
                        return {
                            "valido": False,
                            "mensagem": f"❌ Você já conquistou a rota paralela {rota_paralela.cidadeA.nome} → {rota_paralela.cidadeB.nome}. Um jogador não pode conquistar ambas rotas duplas!",
                            "rota_bloqueada": True,
                            "rota_paralela_id": rota_paralela.id
                        }
        
        # REGRA ESPECÍFICA 2-3 JOGADORES: Apenas uma rota dupla pode ser usada (por qualquer jogador)
        if self.numero_jogadores < 4:
            rota_paralela_conquistada = dupla.obter_rota_conquistada()
            
            if rota_paralela_conquistada:
                return {
                    "valido": False,
                    "mensagem": "Rota bloqueada: rota paralela já conquistada (regra 2-3 jogadores)",
                    "rota_bloqueada": True,
                    "rota_paralela_id": rota_paralela_conquistada.id
                }
        
        # Rota válida
        return {
            "valido": True,
            "mensagem": "Rota válida",
            "rota_bloqueada": False
        }
    
    def processar_conquista(self, rota: 'Rota', jogador: 'Jogador') -> dict:
        """Processa conquista de rota e bloqueia paralela se necessário
        
        Args:
            rota: Rota sendo conquistada
            jogador: Jogador conquistando
            
        Returns:
            dict com resultado: {
                "sucesso": bool,
                "mensagem": str,
                "bloqueou_paralela": bool,
                "rota_bloqueada_id": str (opcional)
            }
        """
        # Valida conquista
        validacao = self.validar_conquista_rota(rota)
        
        if not validacao["valido"]:
            return error_response(
                validacao["mensagem"],
                bloqueou_paralela=False
            )
        
        # Conquista rota
        rota.proprietario = jogador
        rota.ehConcluida = True
        
        # Bloqueia rota paralela se jogo 2-3 jogadores
        bloqueou = False
        rota_bloqueada_id = None
        
        if self.numero_jogadores < 4:
            dupla = self._encontrar_rota_dupla(rota)
            if dupla:
                bloqueou = dupla.bloquear_paralela()
                if bloqueou:
                    # Identifica qual rota foi bloqueada
                    if dupla.rota1.proprietario == "BLOQUEADO":
                        rota_bloqueada_id = dupla.rota1.id
                    elif dupla.rota2.proprietario == "BLOQUEADO":
                        rota_bloqueada_id = dupla.rota2.id
        
        mensagem = f"Rota conquistada por {jogador.nome if hasattr(jogador, 'nome') else jogador}"
        if bloqueou:
            mensagem += f" (rota paralela bloqueada: {rota_bloqueada_id})"
        
        return success_response(
            mensagem,
            bloqueou_paralela=bloqueou,
            rota_bloqueada_id=rota_bloqueada_id
        )
