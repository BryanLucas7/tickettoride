# Convenções de Tipos TypeScript

> **Localização:** `frontend/types/`  
> **Última atualização:** 24/11/2025

## Princípios Gerais

Este projeto segue convenções consistentes para uso de tipos TypeScript, visando:
- **Legibilidade**: Código fácil de entender
- **Manutenibilidade**: Fácil de modificar e estender
- **Type Safety**: Máxima segurança de tipos em compile-time

---

## Quando usar `interface`

Use `interface` para:

### 1. Objetos de Domínio
```typescript
// ✅ Correto
interface Jogador {
  id: string
  nome: string
  cor: string
  pontos: number
}
```

### 2. Props de Componentes React
```typescript
// ✅ Correto
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
}
```

### 3. Contratos de API (Request/Response)
```typescript
// ✅ Correto
interface ApiResponse {
  success: boolean
  data: unknown
  message?: string
}
```

### 4. Return Types de Hooks
```typescript
// ✅ Correto
interface UseGameReturn {
  gameState: GameState | null
  carregando: boolean
  iniciarJogo: () => Promise<void>
}
```

### 5. Objetos que podem ser estendidos
```typescript
// ✅ Correto - interfaces podem ser estendidas
interface BaseEntity {
  id: string
  createdAt: Date
}

interface Jogador extends BaseEntity {
  nome: string
}
```

---

## Quando usar `type`

Use `type` para:

### 1. Union Types
```typescript
// ✅ Correto
type StatusTurno = 'aguardando' | 'jogando' | 'finalizado'
type Resultado = 'sucesso' | 'erro' | 'pendente'
```

### 2. Discriminated Unions
```typescript
// ✅ Correto
type ApiResponse<T> = 
  | { success: true; data: T }
  | { success: false; error: string }
```

### 3. Tipos Utilitários e Aliases
```typescript
// ✅ Correto
type Nullable<T> = T | null
type AsyncFunction = () => Promise<void>
type SetState<T> = React.Dispatch<React.SetStateAction<T>>
```

### 4. Interseções Complexas
```typescript
// ✅ Correto
type JogadorComPontuacao = Jogador & { pontuacaoFinal: number }
```

### 5. Tipos Derivados
```typescript
// ✅ Correto
type JogadorId = Jogador['id']
type CoresDisponiveis = keyof typeof CORES_HEX
```

---

## Quando usar `enum`

Use `enum` para:

### 1. Conjuntos Fixos de Valores
```typescript
// ✅ Correto - valores conhecidos em compile-time
enum CorCarta {
  VERMELHO = 'VERMELHO',
  AZUL = 'AZUL',
  VERDE = 'VERDE'
}
```

### Alternativa: Const Objects (preferido em alguns casos)
```typescript
// ✅ Também correto - mais flexível para tree-shaking
const COR_CARTA = {
  VERMELHO: 'VERMELHO',
  AZUL: 'AZUL',
  VERDE: 'VERDE'
} as const

type CorCarta = typeof COR_CARTA[keyof typeof COR_CARTA]
```

---

## Organização de Arquivos de Tipos

```
frontend/types/
├── index.ts          # Re-exportações públicas centralizadas
├── game.ts           # Entidades do domínio (Jogador, Rota, Carta, GameState)
├── api.ts            # Tipos de request/response da API (DrawCardResponse, etc.)
├── branded.ts        # Branded types (JogadorId, GameId, RotaId, BilheteId)
├── ui.ts             # Tipos específicos de UI/componentes React
└── CONVENTIONS.md    # Este arquivo de documentação
```

### Descrição dos Arquivos

| Arquivo | Responsabilidade | Exemplos |
|---------|-----------------|----------|
| `game.ts` | Entidades de domínio do jogo | `Jogador`, `Rota`, `CartaVagao`, `GameState` |
| `api.ts` | Tipos de comunicação com backend | `DrawCardResponse`, `ConquerRouteResponse`, `ApiError` |
| `branded.ts` | IDs tipados para segurança | `JogadorId`, `GameId`, funções `as*Id()` |
| `ui.ts` | Tipos de componentes React | `PlayerColorConfig`, `LoadingState`, `ModalState` |
| `index.ts` | Re-exportações públicas | Importar de `@/types` para acesso centralizado |

---

## Branded Types (IDs Tipados)

Use Branded Types para IDs de entidades, prevenindo troca acidental:

### Definição
```typescript
// types/branded.ts
declare const __brand: unique symbol
type Brand<T, TBrand extends string> = T & { readonly [__brand]: TBrand }

export type JogadorId = Brand<string, 'JogadorId'>
export type GameId = Brand<string, 'GameId'>
export type RotaId = Brand<string, 'RotaId'>
export type BilheteId = Brand<string, 'BilheteId'>
```

### Uso
```typescript
// ✅ Correto
const jogadorId = asJogadorId("123-abc")
const gameId = asGameId("game-456")

// ❌ Erro de compilação - tipos incompatíveis!
const errado: GameId = jogadorId // Type error!
```

### Funções Helper
```typescript
import { asJogadorId, asGameId, toJogadorId, isValidId } from '@/types'

// Conversão direta (quando você tem certeza que é válido)
const id = asJogadorId("123")

// Conversão com validação (retorna null se inválido)
const idSeguro = toJogadorId(inputDesconhecido) // JogadorId | null

// Type guard para validação
if (isValidId(valor)) {
  const id = asJogadorId(valor)
}
```

---

## Literal Types para Cores

Use Literal Types (Union Types de strings) para cores:

### Tipos Disponíveis
```typescript
// Cores de jogadores
type CorJogador = 'vermelho' | 'azul' | 'verde' | 'amarelo' | 'roxo'

// Cores de cartas de vagão
type CorCartaString = 'vermelho' | 'azul' | 'verde' | 'amarelo' | 'laranja' | 'branco' | 'preto' | 'roxo' | 'locomotiva'

// Cores de rotas (inclui cinza para rotas neutras)
type CorRotaString = 'vermelho' | 'azul' | 'verde' | 'amarelo' | 'laranja' | 'branco' | 'preto' | 'roxo' | 'cinza'

// Union de todas as cores para uso em mapas
type CorMapa = CorJogador | CorCartaString | CorRotaString | 'rosa'
```

### Funções Helper
```typescript
import { obterCorMapa, isCorMapa } from '@/types'

// Obter cor em inglês de forma type-safe
const corIngles = obterCorMapa("vermelho") // "red"
const corFallback = obterCorMapa(null, "gray") // "gray"

// Type guard para verificar cor válida
if (isCorMapa(corString)) {
  // corString é CorMapa aqui
}
```

---

## Padrões de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Interface de Props | `*Props` | `ButtonProps`, `CardProps` |
| Interface de Return | `*Return` | `UseGameReturn` |
| Interface de API Response | `*Response` | `ApiResponse`, `GameStateResponse` |
| Union Type de Status | `Status*` | `StatusTurno`, `StatusJogo` |
| Type Alias | PascalCase | `JogadorId`, `SetState` |

---

## Exemplos Práticos

### ❌ Evitar
```typescript
// Não use type para objetos simples
type Jogador = {
  id: string
  nome: string
}

// Não use interface para unions
interface Status {
  value: 'ativo' | 'inativo'  // Union deveria ser type
}
```

### ✅ Preferir
```typescript
// Use interface para objetos
interface Jogador {
  id: string
  nome: string
}

// Use type para unions
type Status = 'ativo' | 'inativo'
```

---

## Checklist de Revisão

Ao criar novos tipos, verifique:

- [ ] Estou usando `interface` para objetos de domínio?
- [ ] Estou usando `type` para unions?
- [ ] O tipo está no arquivo correto (`game.ts`, `api.ts`, etc.)?
- [ ] A nomenclatura segue o padrão do projeto?
- [ ] O tipo tem documentação JSDoc se for público?
- [ ] Existe duplicação com tipos existentes?
