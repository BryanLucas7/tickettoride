"""
TASK #82: API - Endpoints completos de ações de jogo

Implementa Singleton Pattern para GameManager.

GoF Patterns:
1. Singleton Pattern - GameManager tem única instância

GRASP Principles:
- Controller: Coordena criação e acesso ao jogo
"""

from typing import Optional


class GameManager:
    """
    Singleton Pattern: Gerencia única instância do jogo ativo.

    GoF Singleton Pattern:
    - __instance armazena única instância
    - __new__ garante criação de apenas uma instância
    - get_instance() retorna instância única

    GRASP Controller: Coordena criação e acesso ao jogo
    """

    _instance: Optional['GameManager'] = None
    _jogo: Optional['Jogo'] = None

    def __new__(cls):
        """
        Singleton Pattern: Garante única instância.

        Se instância não existe, cria nova.
        Se já existe, retorna existente.
        """
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'GameManager':
        """
        Retorna instância única do GameManager.

        GoF Singleton Pattern: Método de acesso à instância
        """
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance

    def criar_jogo(self, jogo: 'Jogo') -> bool:
        """Cria novo jogo (substitui jogo anterior se existir)"""
        self._jogo = jogo
        return True

    def obter_jogo(self) -> Optional['Jogo']:
        """Retorna jogo ativo"""
        return self._jogo

    def resetar(self):
        """Reseta GameManager (útil para testes)"""
        self._jogo = None

    @classmethod
    def resetar_singleton(cls):
        """Reseta singleton (útil para testes)"""
        cls._instance = None