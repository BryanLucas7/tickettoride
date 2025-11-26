/**
 * usePlayerData - Hook para dados específicos do jogador
 * 
 * Responsabilidade única: Gerenciar cartas, bilhetes e identificação
 * do jogador atual.
 */

import { useState, useEffect, useCallback, useRef } from "react"
import type { CartaVagao, BilheteDestino, GameState } from "@/types/game"
import { gameApi, ApiError } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import type { UsePlayerDataReturn } from "./types"

interface UsePlayerDataProps {
  gameState: GameState | null
  limparDadosJogo: () => void
  onInvalidData?: () => void
}

export function usePlayerData({
  gameState,
  limparDadosJogo,
  onInvalidData
}: UsePlayerDataProps): UsePlayerDataReturn {
  const [minhasCartas, setMinhasCartas] = useState<CartaVagao[]>([])
  const [meusBilhetes, setMeusBilhetes] = useState<BilheteDestino[]>([])
  const [jogadorAtualId, setJogadorAtualId] = useState<string>("")
  
  const jogadorAtualAnteriorRef = useRef<string | null>(null)
  const invalidPlayerRef = useRef(false)
  
  /**
   * Busca cartas do jogador atual
   */
  const buscarCartas = useCallback(async (gameId: string, playerId: string) => {
    try {
      const cartasData = await gameApi.getPlayerCards(gameId, playerId)
      if (cartasData.cards && Array.isArray(cartasData.cards)) {
        setMinhasCartas(cartasData.cards)
      } else {
        console.warn("Formato de cartas inválido")
        limparDadosJogo()
        onInvalidData?.()
      }
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        setMinhasCartas([])
      } else {
        throw error
      }
    }
  }, [limparDadosJogo, onInvalidData])
  
  /**
   * Busca bilhetes do jogador atual
   */
  const buscarBilhetes = useCallback(async (gameId: string, playerId: string) => {
    try {
      const bilhetesData = await gameApi.getPlayerTickets(gameId, playerId)
      if (bilhetesData.tickets && Array.isArray(bilhetesData.tickets)) {
        setMeusBilhetes(bilhetesData.tickets)
      }
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        setMeusBilhetes([])
      }
    }
  }, [])
  
  /**
   * Atualiza dados quando o gameState muda
   */
  useEffect(() => {
    if (!gameState) return
    
    const gameId = storageService.getGameId()
    const jogadorStorage = storageService.getCurrentPlayer()
    const playerId = jogadorStorage?.id ? String(jogadorStorage.id) : ""

    if (!gameId || !playerId) {
      if (!invalidPlayerRef.current) {
        invalidPlayerRef.current = true
        onInvalidData?.()
      }
      return
    }

    const jogadorInfo = gameState.jogadores?.find((j) => String(j.id) === playerId)
    const numCartasState = jogadorInfo?.num_cartas
    const numBilhetesState = jogadorInfo?.num_bilhetes

    if (!jogadorInfo) {
      if (!invalidPlayerRef.current) {
        invalidPlayerRef.current = true
        onInvalidData?.()
      }
      return
    }

    invalidPlayerRef.current = false
    setJogadorAtualId(playerId)

    const jogadorMudou = jogadorAtualAnteriorRef.current !== playerId
    const cartasDesatualizadas =
      typeof numCartasState === "number" && numCartasState !== minhasCartas.length
    const bilhetesDesatualizados =
      typeof numBilhetesState === "number" && numBilhetesState !== meusBilhetes.length

    if (jogadorMudou || cartasDesatualizadas || minhasCartas.length === 0) {
      buscarCartas(gameId, playerId)
    }
    if (jogadorMudou || bilhetesDesatualizados || meusBilhetes.length === 0) {
      buscarBilhetes(gameId, playerId)
    }

    jogadorAtualAnteriorRef.current = playerId
  }, [
    gameState?.game_id,
    gameState?.jogadores,
    minhasCartas.length,
    meusBilhetes.length,
    buscarCartas,
    buscarBilhetes,
    onInvalidData
  ])
  
  /**
   * Verifica se é a vez do jogador atual (validado com backend)
   *
   * Cada aba guarda o jogador selecionado no localStorage. Aqui
   * comparamos esse id com o jogador da vez informado pelo backend.
   */
  const ehMinhaVez = Boolean(gameState?.jogador_atual_id && gameState.jogador_atual_id === jogadorAtualId)
  
  return {
    minhasCartas,
    meusBilhetes,
    jogadorAtualId,
    ehMinhaVez,
    setMinhasCartas,
    setMeusBilhetes,
    setJogadorAtualId
  }
}
