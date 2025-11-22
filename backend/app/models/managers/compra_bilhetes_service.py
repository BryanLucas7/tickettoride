"""
Compra de Bilhetes Durante o Jogo
==================================

Controller - Coordena ação de compra de bilhetes durante o jogo.

Responsabilidades:
- Iniciar compra de bilhetes
- Validar escolha (mínimo 1)
- Adicionar bilhetes escolhidos ao jogador
- Devolver bilhetes recusados
- Coordenar fluxo completo

GRASP Principles:
- Controller: Coordena ação de compra
- Low Coupling: Usa GerenciadorBilhetesDestino e Jogador
- High Cohesion: Focado em compra de bilhetes durante jogo
"""

from dataclasses import dataclass, field
from typing import List, Dict
from .gerenciador_bilhetes_destino import GerenciadorBilhetesDestino
from .bilhete_destino import BilheteDestino
from .jogador import Jogador


@dataclass
class CompraBilhetesService:
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