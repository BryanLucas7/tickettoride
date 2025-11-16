# Ticket to Ride - Backend

Sistema backend para o jogo Ticket to Ride implementado em Python.

## Estrutura do Projeto

O projeto segue fielmente o diagrama de classes fornecido, com as seguintes classes principais:

### Classes Principais

- **Jogo**: Classe principal que gerencia o estado do jogo
- **Jogador**: Representa um jogador com suas cartas, bilhetes e pontuação
- **Tabuleiro**: Gerencia cidades e rotas do jogo
- **GerenciadorDeTurnos**: Controla a ordem dos turnos entre jogadores
- **GerenciadorDeBaralho**: Gerencia os baralhos de cartas vagão e bilhetes
- **Placar**: Calcula e mantém as pontuações dos jogadores

### Classes de Dados

- **Carta**: Classe base para todas as cartas
- **CartaVagao**: Carta de vagão com cor e indicador de locomotiva
- **BilheteDestino**: Bilhete com origem, destino e pontos
- **Rota**: Conexão entre duas cidades
- **Cidade**: Representa uma cidade no tabuleiro
- **Mao**: Gerencia as cartas na mão de um jogador
- **Baralho**: Pilha de cartas com embaralhamento

### Enumeração

- **Cor**: Cores disponíveis (VERMELHO, AZUL, VERDE, AMARELO, PRETO, LARANJA)

## Como Executar

\`\`\`bash
cd backend/app
python main.py
\`\`\`

## Estrutura de Arquivos

\`\`\`
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── jogo.py
│   │   ├── jogador.py
│   │   ├── tabuleiro.py
│   │   ├── gerenciador_de_turnos.py
│   │   ├── gerenciador_de_baralho.py
│   │   ├── placar.py
│   │   ├── carta.py
│   │   ├── carta_vagao.py
│   │   ├── bilhete_destino.py
│   │   ├── rota.py
│   │   ├── cidade.py
│   │   ├── mao.py
│   │   ├── baralho.py
│   │   └── cor.py
│   └── main.py
└── README.md
\`\`\`

## Regras Implementadas

- Cada jogador começa com 45 vagões
- Baralho de cartas vagão: 12 cartas de cada cor + 14 locomotivas
- Pontuação por comprimento de rota: 1→1, 2→2, 3→4, 4→7, 5→10, 6→15
- Fim de jogo quando um jogador tem 2 ou menos vagões restantes

## Próximos Passos

- Implementar API REST com FastAPI
- Adicionar validações completas de regras
- Implementar verificação de bilhetes concluídos
- Adicionar persistência de dados
- Criar testes unitários
