# Documentação dos Padrões GoF Aplicados
## Ticket to Ride - Projeto de Software

---

## 📋 Índice

1. [Strategy Pattern](#1-strategy-pattern)
2. [Observer Pattern](#2-observer-pattern)
3. [Template Method Pattern](#3-template-method-pattern)
4. [Singleton Pattern](#4-singleton-pattern)
5. [Factory Method Pattern](#5-factory-method-pattern)
6. [State Pattern](#6-state-pattern)
7. [Conclusão](#conclusão)

---

## 1. Strategy Pattern

### Diagrama de Classes

```
┌──────────────────────────────┐
│ <<interface>>                │
│ RotaValidationStrategy       │
│ + validar(...)               │
└─────────────┬────────────────┘
              │ fornece algoritmos
    ┌─────────▼────────┐   ┌──────────▼─────────┐
    │RotaColoridaStrategy│ │RotaCinzaStrategy   │
    └─────────┬────────┘   └──────────┬────────┘
              │ escolhidas via factory
         ┌────▼───────────────────────┐
         │ConquistaRotaController     │
         │+ criar_estrategia_validacao│
         └────────────────────────────┘
```

### Justificativa

- Um controller único delega a validação de rotas para estratégias intercambiáveis, evitando condicionais extensas.
- O factory (`criar_estrategia_validacao`) esconde quais algoritmos existem, permitindo introduzir novas regras sem alterar clientes.
- A combinação Strategy + Factory mantém o fluxo de conquista estável mesmo quando surgem rotas especiais.

### Benefício

- Regras de validação evoluem sem tocar nos controladores, preservando estabilidade e reduzindo o risco de regressões em partidas em andamento.

---

## 2. Observer Pattern

### Diagrama de Classes

```
┌──────────────────────────────┐        notifica        ┌─────────────────┐
│            Placar            │ ─────────────────────▶ │PontuacaoObserver│
│+ registrarObserver()         │                        │+ atualizar(...)  │
│+ adicionarPontos()           │◀───────────────────────┤(Log, Histórico, …)
└──────────────────────────────┘        registra        └─────────────────┘
```

### Justificativa

- O `Placar` concentra a pontuação e expõe um canal de eventos; observers cuidam de log, histórico ou UI sem depender do núcleo.
- Novos observadores são plugados apenas registrando-se, mantendo o acoplamento baixo e a coesão de cada responsabilidade.
- A mesma infraestrutura atende backend e integrações futuras (push, dashboards) sem alterar o sujeito.

### Benefício

- Facilita integrações adicionais (telemetria, UI, alertas) sem modificar o núcleo de pontuação, acelerando novas features e garantindo consistência dos dados.

---

## 3. Template Method Pattern

### Diagrama de Classes

```
┌──────────────────────────────┐
│ <<abstract>> AcaoTurno       │
│+ executar()                  │
│# validar_acao_especifica()   │
│# executar_acao_especifica()  │
└─────────────┬────────────────┘
              │ passos variáveis
 ┌────────────▼──────────┐ ┌────────────▼──────────┐ ┌────────────▼──────────┐
 │AcaoComprarCartas      │ │AcaoConquistarRota      │ │(outras ações de turno)│
 └───────────────────────┘ └───────────────────────┘ └───────────────────────┘
```

### Justificativa

- O método `executar()` fixa o fluxo (validação geral → validação específica → execução → transição de turno).
- Cada subclasse altera apenas os passos específicos, garantindo coerência entre ações e reduzindo duplicação de regras.
- Novas ações entram no jogo respeitando o mesmo pipeline, simplificando testes e regras de negócio.

### Benefício

- Mantém o cumprimento das regras de turno em qualquer nova ação implementada, reduzindo bugs e facilitando auditoria do fluxo de jogo.

---

## 4. Singleton Pattern

### Diagrama de Classes

```
┌──────────────────────────────┐
│        GameManager           │
│- _instance: GameManager      │
│- _jogo: Jogo                 │
│+ get_instance()              │
│+ criar_jogo(jogo: Jogo)      │
│+ obter_jogo()                │
└──────────────────────────────┘
```

### Justificativa

- A camada de API precisa acessar um único jogo ativo; o singleton expõe essa referência de maneira controlada.
- A existência de `resetar_singleton()` facilita cenários de teste e reinicializações do servidor.
- Evita estados duplicados de partida quando múltiplas requisições chegam ao backend.

### Benefício

- Garante uma única fonte de verdade do estado da partida, simplificando sincronização entre endpoints e evitando partidas divergentes para os jogadores.

---

## 5. Factory Method Pattern

### Diagrama de Classes

```
┌──────────────────────────────┐
│     GerenciadorDeBaralho     │
│+ inicializarBaralhoVagoes()  │
│+ inicializarBaralhoBilhetes()│
└─────────────┬────────────────┘
              │ cria coleções
 ┌────────────▼──────────┐   ┌────────────▼──────────┐
 │Baralho (vagões)       │   │Baralho (bilhetes)     │
 └───────────────────────┘   └───────────────────────┘
              │ injeta
        ┌─────▼────────────────┐
        │Jogo / DescarteManager│
        └──────────────────────┘
```

### Justificativa

- Todo o processo de criação, embaralhamento e reposição de cartas fica encapsulado, liberando `Jogo` de detalhes construtivos.
- Permite variar facilmente o baralho (mapas alternativos, eventos) ao substituir apenas o factory.
- Mantém consistência na quantidade de cartas abertas, descarte e reembaralhamento.

### Benefício

- A produção de baralhos padronizada impede erros de configuração (cartas faltando ou sobrando) e acelera ajustes de conteúdo futuro.

---

## 6. State Pattern

### Diagrama de Classes

```
┌──────────────────────────────┐
│        TurnoContext          │
│- state: TurnoState           │
│+ setState(TurnoState)        │
│+ executarAcao(acao)          │
└─────────────┬────────────────┘
              │ delega
     ┌────────▼──────────┐
     │<<interface>>      │
     │TurnoState         │
     └──────┬────────────┘
            │ concretiza
 ┌──────────▼──────────┐ ┌──────────▼──────────┐ ┌──────────▼──────────┐
 │AguardandoAcaoState  │ │AcaoEmAndamentoState │ │AcaoConcluidaState   │
 └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

### Justificativa

- A UI reage às mudanças de estado (aguardando, em andamento, concluído) sem condicionais espalhadas.
- Cada estado conhece somente seu comportamento, promovendo isolamento das regras de habilitação/ações.
- Novos estados ou transições (ex.: pausa, bloqueio) são adicionados criando novas classes, sem alterar o contexto.

### Benefício

- Usuários recebem feedback consistente sobre o turno atual, enquanto o código permanece simples para adicionar novos estados ou efeitos temporários.

---

## Conclusão

| Padrão | Papel no Projeto | Benefício Principal |
|--------|------------------|---------------------|
| Strategy | Validação de rotas coloridas/cinzas | Regras plugáveis e protegidas contra variações |
| Observer | Emissão de eventos de pontuação | Notificações desacopladas e reutilizáveis |
| Template Method | Fluxo das ações de turno | Processo padronizado com passos especializados |
| Singleton | Gestão do jogo ativo no backend | Fonte única de verdade durante a partida |
| Factory Method | Construção dos baralhos do mapa Brasil | Centralização da criação complexa de cartas |
| State | Gestão do turno na camada de UI | Transições explícitas e previsíveis na UI |


