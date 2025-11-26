/**
 * StorageService - Serviço centralizado para acesso ao localStorage
 * 
 * REFATORAÇÃO DRY: Centraliza acesso ao localStorage que estava
 * espalhado em ~10 lugares do código.
 * 
 * GRASP - Pure Fabrication: Utilitário de armazenamento
 * GRASP - Information Expert: Concentra conhecimento sobre keys e formato
 * 
 * Benefícios:
 * - Única fonte de verdade para keys do localStorage
 * - Type-safety para valores armazenados
 * - Facilita mocking em testes
 * - Centraliza tratamento de erros de JSON
 */

import { GAME_STORAGE_KEY } from '@/types/game'
import type { JogadorStorage } from '@/types/api'

// ============================================
// CONSTANTES DE KEYS
// ============================================

export const STORAGE_KEYS = {
  /** ID do jogo atual */
  GAME_ID: GAME_STORAGE_KEY,
  /** Lista de jogadores do jogo atual */
  JOGADORES: 'jogadores',
  /** Jogador selecionado para esta aba */
  CURRENT_PLAYER: 'currentPlayer',
} as const

// ============================================
// TIPOS
// ============================================

export interface GameStorageData {
  gameId: string | null
  jogadores: JogadorStorage[]
  currentPlayer: JogadorStorage | null
}

// ============================================
// SERVIÇO DE STORAGE
// ============================================

/**
 * Serviço centralizado para localStorage
 * 
 * @example
 * ```typescript
 * // Antes (espalhado em ~10 lugares):
 * const gameId = localStorage.getItem('gameId')
 * const jogadores = JSON.parse(localStorage.getItem('jogadores') || '[]')
 * 
 * // Depois (centralizado):
 * const gameId = storageService.getGameId()
 * const jogadores = storageService.getJogadores()
 * ```
 */
export const storageService = {
  // ============================================
  // GAME ID
  // ============================================
  
  /**
   * Retorna o ID do jogo atual
   */
  getGameId(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem(STORAGE_KEYS.GAME_ID)
  },
  
  /**
   * Salva o ID do jogo
   */
  setGameId(gameId: string): void {
    if (typeof window === 'undefined') return
    localStorage.setItem(STORAGE_KEYS.GAME_ID, gameId)
  },
  
  /**
   * Remove o ID do jogo
   */
  removeGameId(): void {
    if (typeof window === 'undefined') return
    localStorage.removeItem(STORAGE_KEYS.GAME_ID)
  },
  
  // ============================================
  // JOGADORES
  // ============================================
  
  /**
   * Retorna a lista de jogadores do jogo atual
   */
  getJogadores(): JogadorStorage[] {
    if (typeof window === 'undefined') return []
    try {
      const data = localStorage.getItem(STORAGE_KEYS.JOGADORES)
      return data ? JSON.parse(data) : []
    } catch {
      console.error('Erro ao ler jogadores do localStorage')
      return []
    }
  },
  
  /**
   * Salva a lista de jogadores
   */
  setJogadores(jogadores: JogadorStorage[]): void {
    if (typeof window === 'undefined') return
    localStorage.setItem(STORAGE_KEYS.JOGADORES, JSON.stringify(jogadores))
  },
  
  /**
   * Remove a lista de jogadores
   */
  removeJogadores(): void {
    if (typeof window === 'undefined') return
    localStorage.removeItem(STORAGE_KEYS.JOGADORES)
  },
  
  /**
   * Retorna um jogador específico por índice
   */
  getJogadorByIndex(index: number): JogadorStorage | null {
    const jogadores = this.getJogadores()
    return jogadores[index] ?? null
  },
  
  /**
   * Retorna um jogador específico por ID
   */
  getJogadorById(id: string): JogadorStorage | null {
    const jogadores = this.getJogadores()
    return jogadores.find(j => j.id === id) ?? null
  },
  
  // ============================================
  // OPERAÇÕES COMPOSTAS
  // ============================================
  
  /**
   * Retorna todos os dados do jogo armazenados
   */
  getGameData(): GameStorageData {
    return {
      gameId: this.getGameId(),
      jogadores: this.getJogadores(),
      currentPlayer: this.getCurrentPlayer()
    }
  },
  
  /**
   * Salva todos os dados do jogo
   */
  setGameData(gameId: string, jogadores: JogadorStorage[]): void {
    this.setGameId(gameId)
    this.setJogadores(jogadores)
    this.removeCurrentPlayer()
    console.log('💾 Dados salvos no localStorage:', {
      gameId,
      numJogadores: jogadores.length
    })
  },
  
  /**
   * Limpa todos os dados do jogo (usado ao criar novo jogo)
   */
  clearGameData(): void {
    console.log('🧹 Limpando dados antigos do localStorage...')
    this.removeGameId()
    this.removeJogadores()
    this.removeCurrentPlayer()
  },

  /**
   * Verifica se há um jogo válido armazenado
   */
  hasValidGame(): boolean {
    const gameId = this.getGameId()
    const jogadores = this.getJogadores()
    return Boolean(gameId && jogadores.length > 0)
  },

  /**
   * Retorna o jogador atual selecionado nesta aba
   */
  getCurrentPlayer(): JogadorStorage | null {
    if (typeof window === 'undefined') return null
    try {
      const data = window.sessionStorage.getItem(STORAGE_KEYS.CURRENT_PLAYER) 
        ?? localStorage.getItem(STORAGE_KEYS.CURRENT_PLAYER)
      return data ? JSON.parse(data) : null
    } catch {
      console.error('Erro ao ler jogador atual do localStorage')
      return null
    }
  },

  /**
   * Define o jogador atual desta aba
   */
  setCurrentPlayer(player: JogadorStorage): void {
    if (typeof window === 'undefined') return
    if (!player?.id) {
      console.warn('Tentativa de salvar jogador atual sem id válido')
      return
    }
    const payload = JSON.stringify(player)
    // sessionStorage para isolar por aba; localStorage como fallback para compatibilidade
    try {
      window.sessionStorage.setItem(STORAGE_KEYS.CURRENT_PLAYER, payload)
    } catch {
      /* ignore sessionStorage errors */
    }
    localStorage.setItem(STORAGE_KEYS.CURRENT_PLAYER, payload)
  },

  /**
   * Remove o jogador atual desta aba
   */
  removeCurrentPlayer(): void {
    if (typeof window === 'undefined') return
    window.sessionStorage.removeItem(STORAGE_KEYS.CURRENT_PLAYER)
    localStorage.removeItem(STORAGE_KEYS.CURRENT_PLAYER)
  },

  /**
   * Retorna apenas o id do jogador atual
   */
  getCurrentPlayerId(): string | null {
    return this.getCurrentPlayer()?.id ?? null
  }
}

// Export default para uso mais simples
export default storageService
