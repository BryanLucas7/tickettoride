/**
 * useGamePolling - Hook para polling e sincronização com backend
 * 
 * Responsabilidade única: Gerenciar o ciclo de vida do polling
 * e manter o estado do jogo sincronizado com o servidor.
 */

import { useState, useEffect, useRef, useCallback } from "react"
import { useRouter } from "next/navigation"
import type { GameState, Jogador } from "@/types/game"
import { gameApi, ApiError } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import type { UseGamePollingReturn } from "./types"

const POLLING_INTERVAL_MS = 2000

export function useGamePolling(): UseGamePollingReturn {
  const router = useRouter()
  
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [carregando, setCarregando] = useState(true)
  
  const currentGameIdRef = useRef<string | null>(null)
  const abortControllerRef = useRef<AbortController | null>(null)
  
  /**
   * Limpa todos os dados do jogo do localStorage e refs
   */
  const limparDadosJogo = useCallback(() => {
    storageService.clearGameData()
    localStorage.removeItem("current_game_id")
    currentGameIdRef.current = null
  }, [])
  
  /**
   * Busca o estado atual do jogo no backend
   */
  const buscarEstadoJogo = useCallback(async (gameId: string) => {
    try {
      // Reset refs se for um novo jogo
      if (currentGameIdRef.current !== gameId) {
        currentGameIdRef.current = gameId
      }

      const state = await gameApi.getGameState(gameId)
      setGameState(state)
      setCarregando(false)
      
    } catch (error) {
      console.error("Erro ao buscar jogo:", error)
      
      if (error instanceof ApiError && error.status === 404) {
        console.warn("Jogo não encontrado (404). Redirecionando para a tela de entrada.")
        limparDadosJogo()
        setCarregando(false)
        router.push("/entrar")
        return
      }
      
      limparDadosJogo()
      setCarregando(false)
      router.push("/entrar")
    }
  }, [limparDadosJogo, router])
  
  /**
   * Inicia polling ao montar o componente
   */
  useEffect(() => {
    const storedGameId = storageService.getGameId()

    if (!storedGameId) {
      setCarregando(false)
      router.push("/entrar")
      return
    }

    // AbortController para cleanup
    abortControllerRef.current = new AbortController()

    // Busca inicial
    buscarEstadoJogo(storedGameId)

    // Polling
    const interval = setInterval(() => {
      const currentGameId = storageService.getGameId()
      if (currentGameId && !abortControllerRef.current?.signal.aborted) {
        buscarEstadoJogo(currentGameId)
      }
    }, POLLING_INTERVAL_MS)

    // Cleanup
    return () => {
      clearInterval(interval)
      abortControllerRef.current?.abort()
    }
  }, [router, buscarEstadoJogo])
  
  return {
    gameState,
    carregando,
    buscarEstadoJogo,
    limparDadosJogo
  }
}
