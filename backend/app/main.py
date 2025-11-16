from models.jogo import Jogo
from models.cidade import Cidade
from models.rota import Rota
from models.jogador import Jogador
from models.cor import Cor
from models.baralho import Baralho
from models.carta_vagao import CartaVagao
from models.gerenciador_de_baralho import GerenciadorDeBaralho

##teste de alteracao git EXCLUIR DPS

def exemplo():
    """Exemplo de uso do sistema Ticket to Ride"""
    
    # Criar cidades
    c1 = Cidade(id="RIO", nome="Rio de Janeiro")
    c2 = Cidade(id="SP", nome="São Paulo")
    c3 = Cidade(id="BH", nome="Belo Horizonte")
    
    # Criar jogo
    jogo = Jogo(id=1)
    
    # Adicionar cidades ao tabuleiro
    jogo.tabuleiro.cidades.extend([c1, c2, c3])
    
    # Criar rotas
    rota1 = Rota(id="r1", cidadeA=c1, cidadeB=c2, cor=Cor.AMARELO, comprimento=3)
    rota2 = Rota(id="r2", cidadeA=c2, cidadeB=c3, cor=Cor.AZUL, comprimento=2)
    jogo.tabuleiro.rotas.extend([rota1, rota2])
    
    # Criar jogadores
    p1 = Jogador(nome="Alice", cor=Cor.VERMELHO)
    p2 = Jogador(nome="Bob", cor=Cor.AZUL)
    
    # Adicionar jogadores ao gerenciador de turnos
    jogo.gerenciadorDeTurnos.adicionarJogador(p1)
    jogo.gerenciadorDeTurnos.adicionarJogador(p2)
    
    # Criar baralho de cartas vagão
    baralho_vagoes = Baralho()
    cores = [Cor.VERMELHO, Cor.AZUL, Cor.VERDE, Cor.AMARELO, Cor.PRETO, Cor.LARANJA]
    
    # Adicionar cartas ao baralho (12 de cada cor + 14 locomotivas)
    for cor in cores:
        for _ in range(12):
            baralho_vagoes.adicionar(CartaVagao(cor=cor, ehLocomotiva=False))
    
    # Adicionar locomotivas
    for _ in range(14):
        baralho_vagoes.adicionar(CartaVagao(cor=Cor.LARANJA, ehLocomotiva=True))
    
    baralho_vagoes.embaralhar()
    
    # Iniciar jogo
    jogo.iniciar()
    jogo.gerenciadorDeBaralho.baralhoVagoes = baralho_vagoes
    
    print("=" * 50)
    print("JOGO TICKET TO RIDE INICIADO")
    print("=" * 50)
    print(f"\nJogador atual: {jogo.gerenciadorDeTurnos.getJogadorAtual().nome}")
    print(f"Cor: {jogo.gerenciadorDeTurnos.getJogadorAtual().cor.value}")
    print(f"\nCidades no tabuleiro: {len(jogo.tabuleiro.cidades)}")
    print(f"Rotas no tabuleiro: {len(jogo.tabuleiro.rotas)}")
    print(f"Cartas no baralho: {len(jogo.gerenciadorDeBaralho.baralhoVagoes.cartas)}")
    
    # Simular algumas jogadas
    print("\n" + "=" * 50)
    print("SIMULANDO JOGADAS")
    print("=" * 50)
    
    # Jogador 1 compra cartas
    print(f"\n{p1.nome} comprando 2 cartas...")
    jogo.jogar("comprar_carta")
    jogo.jogar("comprar_carta")
    print(f"Cartas na mão: {len(p1.mao.cartasVagao)}")
    
    # Próximo turno
    jogo.proximar()
    print(f"\nPróximo jogador: {jogo.gerenciadorDeTurnos.getJogadorAtual().nome}")
    
    # Jogador 2 compra cartas
    print(f"{p2.nome} comprando 2 cartas...")
    jogo.jogar("comprar_carta")
    jogo.jogar("comprar_carta")
    print(f"Cartas na mão: {len(p2.mao.cartasVagao)}")
    
    # Verificar rotas disponíveis
    print(f"\n\nRotas disponíveis: {len(jogo.tabuleiro.obterRotasDisponiveis(None))}")
    
    # Verificar fim de jogo
    print(f"\nFim de jogo? {jogo.validarFimDeJogo()}")
    
    print("\n" + "=" * 50)
    print("EXEMPLO CONCLUÍDO")
    print("=" * 50)

if __name__ == "__main__":
    exemplo()
