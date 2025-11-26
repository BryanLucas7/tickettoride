/**
 * Branded Types para IDs
 * 
 * Este arquivo define tipos "branded" (nominais) para IDs,
 * prevenindo a troca acidental de IDs entre entidades diferentes.
 * 
 * @example
 * // Isso causa erro de compilação:
 * const jogadorId: JogadorId = asJogadorId("123")
 * const gameId: GameId = jogadorId // ❌ Type error!
 * 
 * @module types/branded
 */

// ============================================
// BRANDED TYPE BASE
// ============================================

/**
 * Tipo base para criar branded types
 * A propriedade __brand nunca existe em runtime, apenas em compile-time
 */
declare const __brand: unique symbol

type Brand<T, TBrand extends string> = T & { readonly [__brand]: TBrand }

// ============================================
// BRANDED ID TYPES
// ============================================

/**
 * ID único de jogador
 * @example asJogadorId("550e8400-e29b-41d4-a716-446655440000")
 */
export type JogadorId = Brand<string, 'JogadorId'>

/**
 * ID único de jogo/partida
 * @example asGameId("game-123-abc")
 */
export type GameId = Brand<string, 'GameId'>

/**
 * ID único de rota no mapa
 * @example asRotaId("rota-sp-rj-1")
 */
export type RotaId = Brand<string, 'RotaId'>

/**
 * ID único de bilhete de destino
 * @example asBilheteId("bilhete-001")
 */
export type BilheteId = Brand<string, 'BilheteId'>

// ============================================
// HELPER FUNCTIONS - CASTING SEGURO
// ============================================

/**
 * Converte uma string para JogadorId
 * Use ao receber IDs de jogador da API ou localStorage
 */
export function asJogadorId(id: string): JogadorId {
  return id as JogadorId
}

/**
 * Converte uma string para GameId
 * Use ao receber IDs de jogo da API ou localStorage
 */
export function asGameId(id: string): GameId {
  return id as GameId
}

/**
 * Converte uma string para RotaId
 * Use ao receber IDs de rota da API
 */
export function asRotaId(id: string): RotaId {
  return id as RotaId
}

/**
 * Converte uma string para BilheteId
 * Use ao receber IDs de bilhete da API
 */
export function asBilheteId(id: string): BilheteId {
  return id as BilheteId
}

// ============================================
// TYPE GUARDS
// ============================================

/**
 * Verifica se uma string é um ID válido (não vazio)
 * Pode ser usado antes de converter para branded type
 */
export function isValidId(id: unknown): id is string {
  return typeof id === 'string' && id.length > 0
}

/**
 * Converte string para JogadorId com validação
 * Retorna null se o ID for inválido
 */
export function toJogadorId(id: unknown): JogadorId | null {
  return isValidId(id) ? asJogadorId(id) : null
}

/**
 * Converte string para GameId com validação
 * Retorna null se o ID for inválido
 */
export function toGameId(id: unknown): GameId | null {
  return isValidId(id) ? asGameId(id) : null
}

/**
 * Converte string para RotaId com validação
 * Retorna null se o ID for inválido
 */
export function toRotaId(id: unknown): RotaId | null {
  return isValidId(id) ? asRotaId(id) : null
}

/**
 * Converte string para BilheteId com validação
 * Retorna null se o ID for inválido
 */
export function toBilheteId(id: unknown): BilheteId | null {
  return isValidId(id) ? asBilheteId(id) : null
}
