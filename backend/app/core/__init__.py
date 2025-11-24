"""
Core - Núcleo da aplicação (Hexagonal Architecture)

Este pacote contém a lógica de negócio independente de frameworks e tecnologias.

Estrutura:
- domain/: Entidades de domínio (Jogo, Jogador, Carta, etc.)
- services/: Serviços de aplicação (casos de uso)
- ports/: Interfaces (contratos) para comunicação com o mundo externo
  - repositories/: Interfaces para persistência de dados
  
Princípios:
- Independente de frameworks (FastAPI, Flask, etc.)
- Independente de banco de dados (pickle, SQL, NoSQL, etc.)
- Testável sem dependências externas
- Regras de negócio centralizadas
"""
