/**
 * useBilhetesFlow - Fluxo individual de seleção de bilhetes
 *
 * Agora cada aba representa um jogador específico. O hook
 * usa o jogador salvo no localStorage para buscar os bilhetes
 * iniciais pendentes daquele jogador.
 */

import { useState, useEffect, useCallback } from "react"
import { useRouter } from "next/navigation"
import { gameApi, ApiError } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import { useTicketSelection } from "@/hooks/useTicketSelection"
import type { JogadorStorage } from "@/types/api"

export interface BilheteDestino {
  id: string
  cidadeOrigem: string
  cidadeDestino: string
  pontos: number
}

interface UseBilhetesFlowReturn {
  jogador: JogadorStorage | null
  bilhetesDisponiveis: BilheteDestino[]
  carregando: boolean
  isValidSelection: boolean
  quantidadeSelecionada: number
  isSelected: (id: string) => boolean
  toggleBilhete: (id: string) => void
  confirmarSelecao: () => Promise<void>
}

export function useBilhetesFlow(): UseBilhetesFlowReturn {
  const router = useRouter()
  const [jogador, setJogador] = useState<JogadorStorage | null>(null)
  const [bilhetesDisponiveis, setBilhetesDisponiveis] = useState<BilheteDestino[]>([])
  const [carregando, setCarregando] = useState(true)

  // Hook de seleção
  const {
    bilhetesSelecionados,
    toggleBilhete,
    isValidSelection,
    reset: resetSelecao,
    isSelected,
    quantidadeSelecionada
  } = useTicketSelection({ maxSelection: 3, minSelection: 2 })

  const carregarBilhetes = useCallback(async () => {
    const gameId = storageService.getGameId()
    const jogadorAtual = storageService.getCurrentPlayer()

    if (!gameId || !jogadorAtual?.id) {
      router.push("/entrar")
      return
    }

    setJogador(jogadorAtual)
    setCarregando(true)

    try {
      const data = await gameApi.getInitialTickets(gameId, String(jogadorAtual.id))
      const bilhetes = data.bilhetes || []

      if (!bilhetes.length) {
        router.push("/jogo")
        return
      }

      setBilhetesDisponiveis(bilhetes)
      resetSelecao()
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        // Jogador já escolheu bilhetes ou nenhum ticket pendente
        router.push("/jogo")
        return
      }

      const mensagemErro =
        error instanceof ApiError
          ? error.message
          : "Não foi possível carregar os bilhetes. Verifique sua conexão."
      alert(mensagemErro)
    } finally {
      setCarregando(false)
    }
  }, [router, resetSelecao])

  useEffect(() => {
    carregarBilhetes()
  }, [carregarBilhetes])

  const confirmarSelecao = useCallback(async () => {
    if (!isValidSelection) {
      if (quantidadeSelecionada < 2) {
        alert("Selecione ao menos 2 bilhetes para continuar.")
      } else {
        alert("Você pode manter no máximo 3 bilhetes.")
      }
      return
    }

    const gameId = storageService.getGameId()
    const jogadorAtual = storageService.getCurrentPlayer()

    if (!gameId || !jogadorAtual?.id) {
      router.push("/entrar")
      return
    }

    try {
      await gameApi.confirmInitialTickets(gameId, String(jogadorAtual.id), bilhetesSelecionados)
      storageService.setCurrentPlayer(jogadorAtual)
      router.push("/jogo")
    } catch (error) {
      const mensagemErro =
        error instanceof ApiError
          ? error.message
          : "Erro ao confirmar bilhetes. Tente novamente."
      alert(mensagemErro)
    }
  }, [isValidSelection, quantidadeSelecionada, router, bilhetesSelecionados])

  return {
    jogador,
    bilhetesDisponiveis,
    carregando,
    isValidSelection,
    quantidadeSelecionada,
    isSelected,
    toggleBilhete,
    confirmarSelecao
  }
}
