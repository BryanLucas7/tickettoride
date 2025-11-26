/**
 * useTicketFlow - Hook para fluxo de compra de bilhetes
 * 
 * Responsabilidade única: Gerenciar o modal de bilhetes, seleção
 * e confirmação de compra de bilhetes de destino.
 * 
 * DRY REFACTORING: Usa useToggleSelection para lógica de seleção
 */

import { useState, useCallback } from "react"
import type { BilheteDestino } from "@/types/game"
import { gameApi } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import { useToggleSelection } from "@/hooks/useToggleSelection"
import type { UseTicketFlowReturn, TicketFlowDeps } from "./types"
import { handleTurnComplete, handleApiError } from "./utils"

export function useTicketFlow(deps: TicketFlowDeps): UseTicketFlowReturn {
  const {
    jogadorAtualId,
    acaoCartasBloqueiaOutras,
    buscarEstadoJogo,
    setMensagem
  } = deps
  
  const [mostrarModalBilhetes, setMostrarModalBilhetes] = useState(false)
  const [bilhetesDisponiveis, setBilhetesDisponiveis] = useState<BilheteDestino[]>([])
  const [fluxoBilhetesAtivo, setFluxoBilhetesAtivo] = useState(false)
  const [carregandoBilhetesPreview, setCarregandoBilhetesPreview] = useState(false)
  
  // Usa hook de seleção toggle (mínimo 1 selecionado)
  const {
    selected: bilhetesSelecionados,
    toggle: toggleBilhete,
    reset: resetBilhetes,
    setSelected: setBilhetesSelecionados
  } = useToggleSelection<number>({ min: 1 })
  
  /**
   * Inicia o fluxo de compra de bilhetes
   */
  const iniciarFluxoBilhetes = useCallback(async () => {
    if (acaoCartasBloqueiaOutras) {
      setMensagem("⚠️ Conclua a compra de cartas antes de comprar bilhetes.")
      return
    }

    if (!jogadorAtualId) {
      setMensagem("Selecione seu jogador para continuar.")
      return
    }

    const gameId = storageService.getGameId()
    if (!gameId) return

    setCarregandoBilhetesPreview(true)
    setFluxoBilhetesAtivo(true)

    try {
      const data = await gameApi.getTicketsPreview(gameId, jogadorAtualId)
      if (data.tickets && Array.isArray(data.tickets)) {
        setBilhetesDisponiveis(data.tickets)
        resetBilhetes()
        setMostrarModalBilhetes(true)
      } else {
        setMensagem("❌ Não foi possível obter bilhetes disponíveis.")
        setFluxoBilhetesAtivo(false)
      }
    } catch (error) {
      console.error("Erro ao buscar bilhetes:", error)
      handleApiError(error, setMensagem, "Erro ao buscar bilhetes disponíveis")
      setFluxoBilhetesAtivo(false)
    } finally {
      setCarregandoBilhetesPreview(false)
    }
  }, [acaoCartasBloqueiaOutras, jogadorAtualId, setMensagem, resetBilhetes])
  
  /**
   * Confirma a compra dos bilhetes selecionados
   */
  const confirmarBilhetes = useCallback(async () => {
    if (bilhetesSelecionados.length < 1) {
      setMensagem("❌ Você precisa selecionar pelo menos 1 bilhete.")
      return
    }

    if (!jogadorAtualId) {
      setMensagem("Selecione seu jogador para continuar.")
      return
    }

    const gameId = storageService.getGameId()
    if (!gameId) return

    try {
      const indicesSelecionados = bilhetesSelecionados.map(String)
      const data = await gameApi.buyTickets(gameId, jogadorAtualId, indicesSelecionados)

      if (data.success) {
        setMensagem(`✅ ${data.message}`)
        setMostrarModalBilhetes(false)
        setBilhetesDisponiveis([])
        resetBilhetes()
        setFluxoBilhetesAtivo(false)
        
        await handleTurnComplete(buscarEstadoJogo, setMensagem, gameId, data.next_player, 2000)
      } else {
        setMensagem(`❌ ${data.message || "Erro ao comprar bilhetes."}`)
      }
    } catch (error) {
      console.error("Erro ao confirmar bilhetes:", error)
      handleApiError(error, setMensagem, "Erro ao confirmar bilhetes")
    }
  }, [bilhetesSelecionados, jogadorAtualId, buscarEstadoJogo, setMensagem, resetBilhetes])
  
  /**
   * Toggle seleção de bilhete (wrapper para manter compatibilidade)
   */
  const toggleBilheteSelecionado = useCallback((index: number, _minimo = 1) => {
    // O mínimo já é controlado pelo useToggleSelection
    toggleBilhete(index)
  }, [toggleBilhete])
  
  /**
   * Cancela o fluxo de bilhetes
   */
  const cancelarFluxoBilhetes = useCallback(() => {
    setMostrarModalBilhetes(false)
    setBilhetesDisponiveis([])
    resetBilhetes()
    setFluxoBilhetesAtivo(false)
    setMensagem("Compra de bilhetes cancelada.")
  }, [setMensagem])
  
  return {
    mostrarModalBilhetes,
    bilhetesDisponiveis,
    bilhetesSelecionados,
    fluxoBilhetesAtivo,
    carregandoBilhetesPreview,
    iniciarFluxoBilhetes,
    confirmarBilhetes,
    toggleBilheteSelecionado,
    cancelarFluxoBilhetes,
    setMostrarModalBilhetes,
    setBilhetesSelecionados
  }
}
