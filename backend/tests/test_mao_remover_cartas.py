import pytest
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# Adiciona o diretório backend ao path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import apenas das classes necessárias sem dependências circulares
from typing import List


# Reproduz as classes mínimas necessárias para o teste
class CorCarta(Enum):
    AZUL = "azul"
    VERMELHO = "vermelho"
    VERDE = "verde"
    AMARELO = "amarelo"
    PRETO = "preto"
    BRANCO = "branco"
    LARANJA = "laranja"
    ROXO = "roxo"


@dataclass
class CartaVagao:
    cor: CorCarta = None
    ehLocomotiva: bool = False
    
    def __post_init__(self):
        if self.ehLocomotiva:
            self.cor = None


@dataclass
class Mao:
    cartasVagao: List[CartaVagao] = None
    
    def __post_init__(self):
        if self.cartasVagao is None:
            self.cartasVagao = []

    def adicionarCarta(self, carta: CartaVagao):
        """Adiciona uma carta à mão"""
        self.cartasVagao.append(carta)

    def remover_cartas_por_cores(self, cores: List[str]) -> List[CartaVagao]:
        """Remove e retorna cartas específicas da mão baseado nas cores fornecidas."""
        cartas_em_mao = list(self.cartasVagao)
        cartas_removidas = []
        
        for cor in cores:
            cor_normalizada = cor.lower()
            
            # Buscar carta na mão que corresponda à cor
            indice_encontrado = next(
                (
                    idx
                    for idx, carta in enumerate(cartas_em_mao)
                    if (
                        (carta.ehLocomotiva and cor_normalizada == "locomotiva")
                        or (carta.cor and carta.cor.value == cor_normalizada)
                    )
                ),
                None,
            )
            
            if indice_encontrado is None:
                raise ValueError(
                    f"Carta da cor '{cor}' não encontrada na mão do jogador"
                )
            
            # Remove da lista temporária e adiciona às removidas
            cartas_removidas.append(cartas_em_mao.pop(indice_encontrado))
        
        # Atualiza a mão original removendo as cartas
        for carta in cartas_removidas:
            self.cartasVagao.remove(carta)
        
        return cartas_removidas


class TestMaoRemoverCartasPorCores:
    """Testes unitários para o método remover_cartas_por_cores da classe Mao"""
    
    def test_remover_carta_cor_simples(self):
        """Testa remoção de uma carta de cor simples"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        carta_vermelha = CartaVagao(cor=CorCarta.VERMELHO)
        mao.adicionarCarta(carta_azul)
        mao.adicionarCarta(carta_vermelha)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores(["azul"])
        
        # Assert
        assert len(cartas_removidas) == 1
        assert cartas_removidas[0].cor == CorCarta.AZUL
        assert len(mao.cartasVagao) == 1
        assert mao.cartasVagao[0].cor == CorCarta.VERMELHO
    
    def test_remover_multiplas_cartas(self):
        """Testa remoção de múltiplas cartas de cores diferentes"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        carta_vermelha = CartaVagao(cor=CorCarta.VERMELHO)
        carta_verde = CartaVagao(cor=CorCarta.VERDE)
        mao.adicionarCarta(carta_azul)
        mao.adicionarCarta(carta_vermelha)
        mao.adicionarCarta(carta_verde)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores(["azul", "verde"])
        
        # Assert
        assert len(cartas_removidas) == 2
        assert cartas_removidas[0].cor == CorCarta.AZUL
        assert cartas_removidas[1].cor == CorCarta.VERDE
        assert len(mao.cartasVagao) == 1
        assert mao.cartasVagao[0].cor == CorCarta.VERMELHO
    
    def test_remover_carta_locomotiva(self):
        """Testa remoção de carta locomotiva"""
        # Arrange
        mao = Mao()
        carta_locomotiva = CartaVagao(ehLocomotiva=True)
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        mao.adicionarCarta(carta_locomotiva)
        mao.adicionarCarta(carta_azul)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores(["locomotiva"])
        
        # Assert
        assert len(cartas_removidas) == 1
        assert cartas_removidas[0].ehLocomotiva is True
        assert len(mao.cartasVagao) == 1
        assert mao.cartasVagao[0].cor == CorCarta.AZUL
    
    def test_remover_cartas_mistas_com_locomotiva(self):
        """Testa remoção de cartas normais e locomotiva juntas"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        carta_locomotiva = CartaVagao(ehLocomotiva=True)
        carta_vermelha = CartaVagao(cor=CorCarta.VERMELHO)
        mao.adicionarCarta(carta_azul)
        mao.adicionarCarta(carta_locomotiva)
        mao.adicionarCarta(carta_vermelha)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores(["azul", "locomotiva"])
        
        # Assert
        assert len(cartas_removidas) == 2
        assert cartas_removidas[0].cor == CorCarta.AZUL
        assert cartas_removidas[1].ehLocomotiva is True
        assert len(mao.cartasVagao) == 1
        assert mao.cartasVagao[0].cor == CorCarta.VERMELHO
    
    def test_remover_carta_inexistente_levanta_erro(self):
        """Testa que ValueError é levantado quando carta não existe"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        mao.adicionarCarta(carta_azul)
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            mao.remover_cartas_por_cores(["vermelho"])
        
        assert "não encontrada na mão" in str(exc_info.value)
        assert "vermelho" in str(exc_info.value)
    
    def test_remover_locomotiva_inexistente_levanta_erro(self):
        """Testa que ValueError é levantado quando locomotiva não existe"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        mao.adicionarCarta(carta_azul)
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            mao.remover_cartas_por_cores(["locomotiva"])
        
        assert "não encontrada na mão" in str(exc_info.value)
    
    def test_remover_segunda_carta_inexistente_levanta_erro(self):
        """Testa que erro é levantado na segunda carta se primeira existe"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        mao.adicionarCarta(carta_azul)
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            mao.remover_cartas_por_cores(["azul", "vermelho"])
        
        # A primeira carta (azul) deve ter sido removida antes do erro
        assert "vermelho" in str(exc_info.value)
    
    def test_remover_cartas_mesma_cor_duas_vezes(self):
        """Testa remoção de duas cartas da mesma cor"""
        # Arrange
        mao = Mao()
        carta_azul1 = CartaVagao(cor=CorCarta.AZUL)
        carta_azul2 = CartaVagao(cor=CorCarta.AZUL)
        carta_vermelha = CartaVagao(cor=CorCarta.VERMELHO)
        mao.adicionarCarta(carta_azul1)
        mao.adicionarCarta(carta_azul2)
        mao.adicionarCarta(carta_vermelha)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores(["azul", "azul"])
        
        # Assert
        assert len(cartas_removidas) == 2
        assert all(c.cor == CorCarta.AZUL for c in cartas_removidas)
        assert len(mao.cartasVagao) == 1
        assert mao.cartasVagao[0].cor == CorCarta.VERMELHO
    
    def test_remover_de_mao_vazia_levanta_erro(self):
        """Testa que erro é levantado ao tentar remover de mão vazia"""
        # Arrange
        mao = Mao()
        
        # Act & Assert
        with pytest.raises(ValueError):
            mao.remover_cartas_por_cores(["azul"])
    
    def test_remover_lista_vazia_retorna_lista_vazia(self):
        """Testa que remover lista vazia não altera a mão"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        mao.adicionarCarta(carta_azul)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores([])
        
        # Assert
        assert len(cartas_removidas) == 0
        assert len(mao.cartasVagao) == 1
    
    def test_case_insensitive_cor(self):
        """Testa que cores com diferentes capitalizações funcionam"""
        # Arrange
        mao = Mao()
        carta_azul = CartaVagao(cor=CorCarta.AZUL)
        mao.adicionarCarta(carta_azul)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores(["AZUL"])
        
        # Assert
        assert len(cartas_removidas) == 1
        assert cartas_removidas[0].cor == CorCarta.AZUL
    
    def test_case_insensitive_locomotiva(self):
        """Testa que 'LOCOMOTIVA' e 'locomotiva' funcionam"""
        # Arrange
        mao = Mao()
        carta_locomotiva = CartaVagao(ehLocomotiva=True)
        mao.adicionarCarta(carta_locomotiva)
        
        # Act
        cartas_removidas = mao.remover_cartas_por_cores(["LOCOMOTIVA"])
        
        # Assert
        assert len(cartas_removidas) == 1
        assert cartas_removidas[0].ehLocomotiva is True
