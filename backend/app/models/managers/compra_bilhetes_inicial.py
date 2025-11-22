"""
Compra Inicial de Bilhetes (Setup do Jogo)
==========================================

Controller - Coordena compra inicial de bilhetes (setup do jogo).

Diferença da compra durante jogo:
- Setup inicial: compra 3, escolhe MÍNIMO 2
- Durante jogo: compra 3, escolhe MÍNIMO 1

GRASP Principles:
- Controller: Coordena setup inicial
- Low Coupling: Reutiliza GerenciadorBilhetesDestino
"""

from dataclasses import dataclass, field
from typing import List, Dict
from .gerenciador_bilhetes_destino import GerenciadorBilhetesDestino
from .bilhete_destino import BilheteDestino
from .jogador import Jogador


@dataclass
class CompraBilhetesInicial:
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