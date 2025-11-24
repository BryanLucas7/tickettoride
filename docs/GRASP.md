# Documentação dos Princípios GRASP Aplicados
## Ticket to Ride - Projeto de Software

---

## 📋 Índice

1. [Introdução](#introdução)
2. [Information Expert](#1-information-expert)
3. [Creator](#2-creator)
4. [Controller](#3-controller)
5. [Low Coupling](#4-low-coupling)
6. [High Cohesion](#5-high-cohesion)
7. [Polymorphism](#6-polymorphism)
8. [Pure Fabrication](#7-pure-fabrication)
9. [Indirection](#8-indirection)
10. [Protected Variations](#9-protected-variations)
11. [Mapeamento Completo](#mapeamento-completo)
12. [Conclusão](#conclusão)


## 1. Information Expert

### Diagrama de Classes

```
┌─────────────┐ possui ┌───────────┐ possui ┌──────────────┐
│   Jogador   │──────▶│   Mao     │──────▶│ CartaVagao / │
│- trens      │      │- cartas   │      │ BilheteDestino│
│- bilhetes   │      └───────────┘      └──────────────┘
│- mao        │
└─────────────┘
```

### Justificativa

- Cada entidade mantém os dados que precisa para operar (jogador gerencia trens/cartas, `Mao` gerencia agrupamentos, componentes visuais conhecem a apresentação).
- A lógica permanece onde as informações residem, reduzindo consultas externas e mantendo consistência de estado.
- Esse desenho garante que qualquer alteração nas regras do jogador impacte apenas os especialistas, não os consumidores.

### Benefício

- Atualizações de regras de jogador ou UI acontecem sem sincronizações extras, prevenindo estados inconsistentes e bugs de domínio.

---

## 2. Creator

### Diagrama de Classes

```
┌──────────┐ cria ┌────────────────────┐
│   Jogo   │────▶│GerenciadorDeBaralho│
│          │     │Placar               │
│          │     │GerenciadorTurnos    │
└──────────┘     └────────────────────┘
        │ delega criação detalhada
        ▼
┌──────────────────────────┐
│GerenciadorDeBaralho      │
│+ inicializarBaralho...   │
└──────────────────────────┘
```

### Justificativa

- `Jogo` é responsável pelo ciclo de vida da partida, portanto instancia os elementos que agrupa e coordena.
- `GerenciadorDeBaralho` conhece o conteúdo dos baralhos e é o ponto natural para criá-los e embaralhá-los.
- A responsabilidade de criação segue a posse/composição, evitando construtores gigantes em outras camadas.

### Benefício

- O ciclo de vida do tabuleiro fica concentrado em poucos pontos, facilitando inicializações reproduzíveis em testes e novas configurações de mapa.

---

## 3. Controller

### Diagrama de Classes

```
┌────────────────┐ orquestra ┌────────────────────┐
│ConquistaRotaCtl│──────────▶│ estratégias / placas│
└────────────────┘           └────────────────────┘
        ▲                             ▲
        │                             │
┌───────────────┐ coordena   ┌──────────────────────┐
│ RouteService  │──────────▶│ Validações específicas│
└───────────────┘            └──────────────────────┘

> **Nota**: `AcaoTurno` foi removido; serviços especializados (RouteConquestService, etc.) agora coordenam ações.

Camada de UI
┌───────────────┐ media ┌───────────────┐
│ GameContext   │──────▶│ gameApiClient │
└───────────────┘       └───────────────┘
```

### Justificativa

- Controladores recebem eventos do sistema e coordenam serviços especializados sem assumir regras de baixo nível.
- `RouteConquestService` e outros serviços garantem o fluxo das ações; `ConquistaRotaController` integra validação, descarte, placar e verificação de fim.
- Na camada de UI, `GameContext` concentra chamadas à API e atualização de estado, mantendo componentes puros.

### Benefício

- Novas operações entram conectando-se ao mesmo controlador, garantindo rastreabilidade do fluxo e permitindo instrumentação centralizada.

---

## 4. Low Coupling

### Diagrama de Classes

```
┌────────────────┐ usa ┌────────────────────┐
│ConquistaRotaCtl│────▶│RotaValidationStrategy│
│                │     │ValidadorRotasDuplas │
│                │     │Placar / FimDeJogo   │
└────────────────┘     └────────────────────┘

Camada de UI
┌─────────────┐ chama ┌──────────────┐
│Componentes  │──────▶│GameContext   │
└─────────────┘       └──────────────┘
```

### Justificativa

- Dependências são injetadas via interfaces, permitindo testar controladores em isolamento e trocar implementações sem refatorar.
- Componentes React apenas recebem dados/handlers; não conhecem HTTP, regras de turno ou instâncias globais.
- Baixo acoplamento facilita evoluções como modos de jogo alternativos ou integrações com IA.

### Benefício

- Trocas de dependências (ex.: novos validadores ou APIs) ocorrem rapidamente, acelerando testes automatizados e adaptações para novas plataformas.

---

## 5. High Cohesion

### Diagrama de Classes

```
┌─────────────┐      ┌───────────────┐
│   Placar    │◀────▶│ Observers     │
│(pontuação)  │      │(log, histórico│
└─────────────┘      └───────────────┘

┌────────────────┐
│ContadorTrens   │
│(UI focada em   │
│trens restantes)│
└────────────────┘
```

### Justificativa

- `Placar` concentra todo o comportamento de pontuação e notificações, evitando responsabilidades espalhadas.
- Componentes visuais, como `ContadorTrens` ou `MaoCartas`, cuidam exclusivamente da renderização do dado que exibem.
- A alta coesão reduz efeitos colaterais e torna cada unidade mais simples de testar e evoluir.

### Benefício

- Cada unidade tem foco claro, facilitando leitura, manutenção e otimizações independentes sem quebrar funcionalidades relacionadas.

---

## 6. Polymorphism

### Diagrama de Classes

```
┌────────────────────────────┐
│<<interface>>               │
│RotaValidationStrategy      │
└─────────────┬──────────────┘
      ┌────────▼──────────┐   ┌────────▼──────────┐
      │RotaColoridaStrategy│ │RotaCinzaStrategy   │
      └────────────────────┘ └────────────────────┘

Estados na UI
┌────────────────┐
│<<interface>>   │
│TurnoState      │
└──────┬─────────┘
   ┌───▼──────────┐ ...
   │Aguardando... │
```

### Justificativa

- Comportamentos que variam por tipo são encapsulados em implementações diferentes, mantendo os clientes agnósticos.
- `ConquistaRotaController` conversa apenas com a interface de validação, e o contexto de turno vê apenas `TurnoState`.
- A adição de novos algoritmos ou estados não toca no código que consome as abstrações.

### Benefício

- Expande-se o jogo com novos estados ou validadores sem alterar clientes, reduzindo riscos de regressão e mantendo regras claras.

---

## 7. Pure Fabrication

### Diagrama de Classes

```
┌──────────────┐
│ Pathfinder   │  (serviço BFS)
└──────────────┘
┌──────────────┐
│ LongestPath  │  (serviço DFS)
└──────────────┘
┌──────────────┐
│ HttpClient   │  (serviço HTTP)
└──────────────┘
```

### Justificativa

- Serviços utilitários encapsulam algoritmos e infraestrutura que não pertencem ao domínio (busca de caminhos, comunicação HTTP).
- Mantém coesão alta nos modelos principais e reduz duplicação de lógica complexa.
- Substituições ou otimizações desses serviços não impactam regras de negócio.

### Benefício

- Serviços técnicos podem evoluir (performance, protocolos) de forma isolada, preservando o domínio principal e agilizando manutenções.

---

## 8. Indirection

### Diagrama de Classes

```
┌───────────────┐     mediam      ┌────────────┐
│Componentes UI │───────────────▶│GameContext │
└───────────────┘                └────┬───────┘
                                      │ chama
                                ┌─────▼─────────┐
                                │GameApiClient  │
                                └─────┬─────────┘
                                      │ usa
                                ┌─────▼─────────┐
                                │HttpClient     │
                                └───────────────┘
```

### Justificativa

- O contexto de jogo e o cliente da API atuam como intermediários, escondendo detalhes de rede e estado global.
- Componentes consumem métodos de alto nível (`conquistarRota`), não endpoints ou tokens.
- Essa camada facilita mocking em testes e substituições futuras (ex.: WebSocket, gRPC) sem afetar a UI.

### Benefício

- A UI permanece enxuta e testável enquanto mudanças de backend ou transporte são absorvidas pela camada intermediária.

---

## 9. Protected Variations

### Diagrama de Classes

```
┌────────────────────────────┐
│ Interfaces estáveis        │
│- RotaValidationStrategy    │
│- TurnoState                │
│- PainelBilhetesDestinoProps│
└─────────────┬──────────────┘
              │ implementações variam livres
      ┌───────▼────────┐   ┌──────────▼─────────┐
      │Strategies novas│   │Estados/Layouts novos│
      └────────────────┘   └────────────────────┘
```

### Justificativa

- Interfaces fixas protegem o restante do sistema quando surgem novas regras de rota, estados de turno ou modos de exibição.
- Variações são confinadas aos pontos de extensão, reduzindo regressões.
- O mapeamento de props (ex.: modo secreto de bilhetes) garante que mudanças de apresentação não quebrem consumidores antigos.

### Benefício

- Novas regras ou layouts chegam por implementações alternativas, mantendo APIs estáveis e reduzindo impactos em clientes existentes.

---

## Mapeamento Completo

| Princípio | Principais Classes/Componentes |
|-----------|--------------------------------|
| Information Expert | `Jogador`, `Mao`, `Placar`, `MaoCartas`, `ContadorTrens` |
| Creator | `Jogo`, `GerenciadorDeBaralho`, `DescarteManager` |
| Controller | `RouteConquestService`, `TicketPurchaseService`, `ConquistaRotaController`, `GameContext` |
| Low Coupling | `ConquistaRotaController`, `GameApiClient`, componentes React |
| High Cohesion | `Placar`, `GerenciadorFimDeJogo`, componentes de UI especializados |
| Polymorphism | `RotaValidationStrategy`, `TurnoState` |
| Pure Fabrication | `Pathfinder`, `LongestPath`, `HttpClient` |
| Indirection | `GameContext`, `GameApiClient`, hooks `useGame` |
| Protected Variations | `RotaValidationStrategy`, `TurnoState`, props de componentes configuráveis |

---

## Conclusão

Os princípios GRASP permanecem aplicados de forma consistente, agora documentados de maneira sucinta:

1. **Information Expert** garante que dados sejam manipulados por quem os conhece.
2. **Creator** mantém o ciclo de vida dos agregados sob as classes que os compõem.
3. **Controller** coordena fluxos complexos, tanto no backend quanto na UI.
4. **Low Coupling** e **High Cohesion** caminham juntos para preservar manutenibilidade.
5. **Polymorphism**, **Pure Fabrication** e **Indirection** criam pontos de extensão seguros.
6. **Protected Variations** blindam o sistema diante de novas regras ou modos de exibição.

**Autores**: Equipe de Desenvolvimento  
**Data**: Novembro 2025  
**Versão**: 1.1
