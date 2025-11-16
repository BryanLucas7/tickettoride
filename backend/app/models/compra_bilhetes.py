"""
TASK #104: Ação: Comprar bilhetes de destino (durante jogo)
=============================================================

PADRÃO GRASP: Information Expert
- GerenciadorBilhetesDestino conhece pilha de bilhetes → gerencia compra
- Jogador conhece seus bilhetes → adiciona bilhetes escolhidos

PADRÃO GRASP: Controller
- CompraBilhetesService coordena ação de compra
- Valida regras (mínimo 1 escolhido)
- Gerencia devolução de bilhetes recusados

PADRÃO GRASP: Low Coupling
- Service não depende de UI
- UI chama service via API

Regras Ticket to Ride - Compra de Bilhetes Durante Jogo:
1. Jogador pode usar turno para comprar bilhetes
2. Compra 3 bilhetes do topo da pilha
3. Deve escolher MÍNIMO 1 (pode escolher 1, 2 ou 3)
4. Bilhetes recusados voltam ao FINAL da pilha
5. Bilhetes escolhidos vão para a mão do jogador
6. Se pilha tiver < 3, compra os que tiver
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .baralho import Baralho
from .bilhete_destino import BilheteDestino, BILHETES_DESTINO
from .jogador import Jogador


@dataclass
class GerenciadorBilhetesDestino:
    """
    Information Expert - Gerencia pilha de bilhetes de destino.
    
    Responsabilidades:
    - Manter pilha de bilhetes de destino
    - Distribuir bilhetes para compra
    - Receber bilhetes devolvidos
    - Verificar quantidade disponível
    
    GRASP Principles:
    - Information Expert: Conhece pilha de bilhetes
    - High Cohesion: Focado em gerenciar bilhetes de destino
    """
    
    pilha: Baralho = field(default_factory=Baralho)
    
    def __post_init__(self):
        """Inicializa pilha com todos os bilhetes"""
        if not self.pilha.cartas:
            self.pilha.cartas = BILHETES_DESTINO.copy()
            self.pilha.embaralhar()
    
    def comprar_bilhetes_para_escolha(self, quantidade: int = 3) -> List[BilheteDestino]:
        """
        Compra bilhetes do topo da pilha para o jogador escolher.
        
        Args:
            quantidade: Quantidade de bilhetes a comprar (padrão: 3)
            
        Returns:
            Lista de bilhetes disponíveis para escolha
            
        Nota: Se pilha tiver menos que a quantidade solicitada,
              retorna todos os disponíveis.
        """
        bilhetes_comprados = []
        
        # Comprar até a quantidade solicitada ou até acabar a pilha
        for _ in range(min(quantidade, len(self.pilha.cartas))):
            bilhete = self.pilha.comprar()
            if bilhete:
                bilhetes_comprados.append(bilhete)
        
        return bilhetes_comprados
    
    def devolver_bilhetes(self, bilhetes: List[BilheteDestino]):
        """
        Devolve bilhetes recusados ao final da pilha.
        
        Args:
            bilhetes: Lista de bilhetes a devolver
        """
        for bilhete in bilhetes:
            self.pilha.adicionar(bilhete, endOf=True)
    
    def quantidade_disponivel(self) -> int:
        """Retorna quantidade de bilhetes disponíveis na pilha"""
        return len(self.pilha.cartas)
    
    def resetar(self):
        """Reseta pilha com todos os bilhetes embaralhados"""
        self.pilha.cartas = BILHETES_DESTINO.copy()
        self.pilha.embaralhar()


@dataclass
class CompraBilhetesService:
    """
    Controller - Coordena ação de compra de bilhetes.
    
    Responsabilidades:
    - Iniciar compra de bilhetes
    - Validar escolha (mínimo 1)
    - Adicionar bilhetes escolhidos ao jogador
    - Devolver bilhetes recusados
    - Coordenar fluxo completo
    
    GRASP Principles:
    - Controller: Coordena ação de compra
    - Low Coupling: Usa GerenciadorBilhetesDestino e Jogador
    - High Cohesion: Focado em compra de bilhetes
    """
    
    gerenciador_bilhetes: GerenciadorBilhetesDestino = field(default_factory=GerenciadorBilhetesDestino)
    
    def iniciar_compra(self, quantidade: int = 3) -> Dict:
        """
        Inicia processo de compra de bilhetes.
        
        Compra bilhetes do topo da pilha para jogador escolher.
        
        Args:
            quantidade: Quantidade de bilhetes a comprar (padrão: 3)
            
        Returns:
            Dicionário com:
            - bilhetes: Lista de bilhetes disponíveis
            - quantidade: Quantidade de bilhetes comprados
            - mensagem: Mensagem informativa
        """
        bilhetes = self.gerenciador_bilhetes.comprar_bilhetes_para_escolha(quantidade)
        
        if not bilhetes:
            return {
                'bilhetes': [],
                'quantidade': 0,
                'mensagem': '⚠️ Pilha de bilhetes vazia!'
            }
        
        mensagem = f"🎯 Escolha no mínimo 1 bilhete (máximo {len(bilhetes)})"
        
        return {
            'bilhetes': bilhetes,
            'quantidade': len(bilhetes),
            'mensagem': mensagem
        }
    
    def confirmar_escolha(
        self,
        jogador: Jogador,
        bilhetes_disponiveis: List[BilheteDestino],
        indices_escolhidos: List[int]
    ) -> Dict:
        """
        Confirma escolha de bilhetes pelo jogador.
        
        Valida escolha, adiciona bilhetes ao jogador e devolve recusados.
        
        Args:
            jogador: Jogador que está comprando
            bilhetes_disponiveis: Lista de bilhetes disponíveis
            indices_escolhidos: Índices dos bilhetes escolhidos
            
        Returns:
            Dicionário com:
            - sucesso: True se escolha válida
            - bilhetes_escolhidos: Bilhetes adicionados ao jogador
            - bilhetes_recusados: Bilhetes devolvidos
            - mensagem: Mensagem de resultado
        """
        # Validar: mínimo 1 bilhete
        if not indices_escolhidos:
            return {
                'sucesso': False,
                'bilhetes_escolhidos': [],
                'bilhetes_recusados': [],
                'mensagem': '❌ Você deve escolher no mínimo 1 bilhete!'
            }
        
        # Validar: índices válidos
        if not all(0 <= i < len(bilhetes_disponiveis) for i in indices_escolhidos):
            return {
                'sucesso': False,
                'bilhetes_escolhidos': [],
                'bilhetes_recusados': [],
                'mensagem': '❌ Índices de bilhetes inválidos!'
            }
        
        # Separar escolhidos e recusados
        bilhetes_escolhidos = [bilhetes_disponiveis[i] for i in indices_escolhidos]
        bilhetes_recusados = [
            bilhete 
            for i, bilhete in enumerate(bilhetes_disponiveis) 
            if i not in indices_escolhidos
        ]
        
        # Adicionar bilhetes ao jogador
        for bilhete in bilhetes_escolhidos:
            jogador.bilhetes.append(bilhete)
        
        # Devolver bilhetes recusados
        self.gerenciador_bilhetes.devolver_bilhetes(bilhetes_recusados)
        
        mensagem_escolhidos = '\n'.join([
            f"  • {b.cidadeOrigem.nome} → {b.cidadeDestino.nome} ({b.pontos} pts)"
            for b in bilhetes_escolhidos
        ])
        
        mensagem = (
            f"✅ {len(bilhetes_escolhidos)} bilhete(s) adicionado(s)!\n"
            f"{mensagem_escolhidos}\n"
            f"({len(bilhetes_recusados)} devolvido(s))"
        )
        
        return {
            'sucesso': True,
            'bilhetes_escolhidos': bilhetes_escolhidos,
            'bilhetes_recusados': bilhetes_recusados,
            'quantidade_escolhidos': len(bilhetes_escolhidos),
            'quantidade_recusados': len(bilhetes_recusados),
            'mensagem': mensagem
        }
    
    def comprar_bilhetes_completo(
        self,
        jogador: Jogador,
        indices_escolhidos: List[int],
        quantidade_inicial: int = 3
    ) -> Dict:
        """
        Executa compra completa de bilhetes em uma única chamada.
        
        Útil para testes ou APIs síncronas.
        
        Args:
            jogador: Jogador que está comprando
            indices_escolhidos: Índices dos bilhetes a escolher (0-2)
            quantidade_inicial: Quantidade de bilhetes a comprar (padrão: 3)
            
        Returns:
            Dicionário com resultado da compra
        """
        # 1. Iniciar compra
        resultado_inicio = self.iniciar_compra(quantidade_inicial)
        
        if not resultado_inicio['bilhetes']:
            return resultado_inicio
        
        # 2. Confirmar escolha
        resultado_confirmacao = self.confirmar_escolha(
            jogador=jogador,
            bilhetes_disponiveis=resultado_inicio['bilhetes'],
            indices_escolhidos=indices_escolhidos
        )
        
        return resultado_confirmacao


@dataclass
class CompraBilhetesInicial:
    """
    Controller - Coordena compra inicial de bilhetes (setup do jogo).
    
    Diferença da compra durante jogo:
    - Setup inicial: compra 3, escolhe MÍNIMO 2
    - Durante jogo: compra 3, escolhe MÍNIMO 1
    
    GRASP Principles:
    - Controller: Coordena setup inicial
    - Low Coupling: Reutiliza GerenciadorBilhetesDestino
    """
    
    gerenciador_bilhetes: GerenciadorBilhetesDestino = field(default_factory=GerenciadorBilhetesDestino)
    
    def iniciar_compra_inicial(self) -> Dict:
        """
        Inicia compra inicial de bilhetes (setup).
        
        Returns:
            Dicionário com bilhetes disponíveis
        """
        bilhetes = self.gerenciador_bilhetes.comprar_bilhetes_para_escolha(3)
        
        return {
            'bilhetes': bilhetes,
            'quantidade': len(bilhetes),
            'mensagem': '🎯 Escolha no mínimo 2 bilhetes para começar'
        }
    
    def confirmar_escolha_inicial(
        self,
        jogador: Jogador,
        bilhetes_disponiveis: List[BilheteDestino],
        indices_escolhidos: List[int]
    ) -> Dict:
        """
        Confirma escolha inicial (MÍNIMO 2).
        
        Args:
            jogador: Jogador que está escolhendo
            bilhetes_disponiveis: Lista de bilhetes disponíveis
            indices_escolhidos: Índices dos bilhetes escolhidos
            
        Returns:
            Dicionário com resultado
        """
        # Validar: mínimo 2 bilhetes
        if len(indices_escolhidos) < 2:
            return {
                'sucesso': False,
                'bilhetes_escolhidos': [],
                'bilhetes_recusados': [],
                'mensagem': '❌ Você deve escolher no mínimo 2 bilhetes no início!'
            }
        
        # Validar: índices válidos
        if not all(0 <= i < len(bilhetes_disponiveis) for i in indices_escolhidos):
            return {
                'sucesso': False,
                'bilhetes_escolhidos': [],
                'bilhetes_recusados': [],
                'mensagem': '❌ Índices de bilhetes inválidos!'
            }
        
        # Separar escolhidos e recusados
        bilhetes_escolhidos = [bilhetes_disponiveis[i] for i in indices_escolhidos]
        bilhetes_recusados = [
            bilhete 
            for i, bilhete in enumerate(bilhetes_disponiveis) 
            if i not in indices_escolhidos
        ]
        
        # Adicionar bilhetes ao jogador
        for bilhete in bilhetes_escolhidos:
            jogador.bilhetes.append(bilhete)
        
        # Devolver bilhetes recusados
        self.gerenciador_bilhetes.devolver_bilhetes(bilhetes_recusados)
        
        mensagem = f"✅ {len(bilhetes_escolhidos)} bilhete(s) inicial(is) escolhido(s)!"
        
        return {
            'sucesso': True,
            'bilhetes_escolhidos': bilhetes_escolhidos,
            'bilhetes_recusados': bilhetes_recusados,
            'mensagem': mensagem
        }
