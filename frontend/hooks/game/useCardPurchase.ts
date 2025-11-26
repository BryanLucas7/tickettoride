/**
 * useCardPurchase - Hook para fluxo de compra de cartas
 * 
 * Responsabilidade única: Gerenciar a compra de cartas abertas e fechadas,
 * incluindo regras de locomotivas e turnos.
 * 
 * Refatorado para usar useReducer ao invés de múltiplos useState,
 * centralizando todas as transições de estado em um único lugar.
 */

import { useReducer, useCallback, useEffect, useRef } from "react"
import type { GameState, CartaVagao } from "@/types/game"
import { gameApi } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import type { UseCardPurchaseReturn, CardPurchaseDeps } from "./types"
import { handleTurnComplete, extractErrorMessage } from "./utils"

// ============================================
// TIPOS DO REDUCER
// ============================================

interface CardPurchaseState {
  cartasCompradasNesteTurno: number
  turnoCompraCompleto: boolean
  bloquearLocomotivaAberta: boolean
  mensagemCompraCartas: string | null
}

type CardPurchaseAction =
  | { type: 'RESET_TURNO' }
  | { type: 'COMPRA_CARTA_FECHADA_SUCESSO'; ehLocomotiva: boolean; turnoFinalizado: boolean }
  | { type: 'COMPRA_CARTA_ABERTA_SUCESSO'; ehLocomotiva: boolean; turnoFinalizado: boolean }
  | { type: 'SET_MENSAGEM'; mensagem: string | null }
  | { type: 'BLOQUEIO_BARALHO_VAZIO' }
  | { type: 'BLOQUEIO_LOCOMOTIVA' }
  | { type: 'ERRO'; mensagem: string }

// ============================================
// MENSAGENS DE ESTADO
// ============================================

const MENSAGENS = {
  TURNO_COMPLETO: "Turno de compra concluído. Aguarde o próximo movimento.",
  TURNO_COMPLETO_JOGADOR: "Turno de compra concluído. Aguarde o próximo jogador.",
  LOCOMOTIVA_FECHADA: "Locomotiva comprada do baralho fechado continua permitindo uma segunda carta. Locomotivas visíveis permanecem bloqueadas.",
  CARTA_COMPRADA: "Você já comprou uma carta. Locomotivas visíveis ficam bloqueadas, mas é permitido pegar outra carta fechada ou uma aberta que não seja locomotiva.",
  LOCOMOTIVA_ABERTA: "Locomotiva visível comprada: essa escolha encerra sua ação de compra de cartas neste turno.",
  UMA_CARTA_COMPRADA: "Você já comprou 1 carta. Locomotivas visíveis ficam bloqueadas até o final do turno.",
  BARALHO_VAZIO: "Baralho esgotado: não há cartas fechadas para comprar no momento.",
  LOCOMOTIVA_BLOQUEADA: "Locomotivas visíveis estão bloqueadas porque você já comprou uma carta neste turno.",
  CARTA_INDISPONIVEL: "Carta indisponível. Aguarde atualização das cartas visíveis.",
  ERRO_CONEXAO: "Não foi possível comprar carta. Verifique sua conexão e tente novamente."
} as const

// ============================================
// ESTADO INICIAL
// ============================================

const initialState: CardPurchaseState = {
  cartasCompradasNesteTurno: 0,
  turnoCompraCompleto: false,
  bloquearLocomotivaAberta: false,
  mensagemCompraCartas: null
}

const normalizarCarta = (carta: any): CartaVagao => ({
  cor: String(carta?.cor || "").toLowerCase() as CartaVagao["cor"],
  eh_locomotiva: carta?.eh_locomotiva === true
})

// ============================================
// REDUCER
// ============================================

/**
 * Reducer centralizado para todas as transições de estado de compra de cartas.
 * 
 * Benefícios:
 * - Todas as transições de estado em um único lugar
 * - Mais fácil de testar (função pura)
 * - Elimina estados inconsistentes
 * - Melhor documentação das transições válidas
 */
function cardPurchaseReducer(
  state: CardPurchaseState,
  action: CardPurchaseAction
): CardPurchaseState {
  switch (action.type) {
    case 'RESET_TURNO':
      return initialState

    case 'COMPRA_CARTA_FECHADA_SUCESSO':
      if (action.turnoFinalizado) {
        return {
          cartasCompradasNesteTurno: 0,
          turnoCompraCompleto: true,
          bloquearLocomotivaAberta: true,
          mensagemCompraCartas: MENSAGENS.TURNO_COMPLETO
        }
      }
      return {
        ...state,
        cartasCompradasNesteTurno: state.cartasCompradasNesteTurno + 1,
        bloquearLocomotivaAberta: true,
        mensagemCompraCartas: action.ehLocomotiva
          ? MENSAGENS.LOCOMOTIVA_FECHADA
          : MENSAGENS.CARTA_COMPRADA
      }

    case 'COMPRA_CARTA_ABERTA_SUCESSO':
      if (action.ehLocomotiva) {
        return {
          cartasCompradasNesteTurno: 0,
          turnoCompraCompleto: true,
          bloquearLocomotivaAberta: true,
          mensagemCompraCartas: MENSAGENS.LOCOMOTIVA_ABERTA
        }
      }
      if (action.turnoFinalizado) {
        return {
          cartasCompradasNesteTurno: 0,
          turnoCompraCompleto: true,
          bloquearLocomotivaAberta: true,
          mensagemCompraCartas: MENSAGENS.TURNO_COMPLETO_JOGADOR
        }
      }
      return {
        ...state,
        cartasCompradasNesteTurno: state.cartasCompradasNesteTurno + 1,
        bloquearLocomotivaAberta: true,
        mensagemCompraCartas: MENSAGENS.UMA_CARTA_COMPRADA
      }

    case 'SET_MENSAGEM':
    case 'ERRO':
      // SET_MENSAGEM e ERRO têm o mesmo comportamento: atualizar apenas a mensagem
      return {
        ...state,
        mensagemCompraCartas: action.mensagem
      }

    case 'BLOQUEIO_BARALHO_VAZIO':
      return {
        ...state,
        mensagemCompraCartas: MENSAGENS.BARALHO_VAZIO
      }

    case 'BLOQUEIO_LOCOMOTIVA':
      return {
        ...state,
        mensagemCompraCartas: MENSAGENS.LOCOMOTIVA_BLOQUEADA
      }

    default:
      return state
  }
}

// ============================================
// HOOK PRINCIPAL
// ============================================

export function useCardPurchase(deps: CardPurchaseDeps): UseCardPurchaseReturn {
  const {
    gameState,
    jogadorAtualId,
    fluxoBilhetesAtivo,
    carregandoBilhetesPreview,
    buscarEstadoJogo,
    setMensagem,
    setMinhasCartas
  } = deps

  const [state, dispatch] = useReducer(cardPurchaseReducer, initialState)
  const jogadorAtualAnteriorRef = useRef<string | null>(null)

  // Valores computados
  const fluxoCompraCartasAtivo = state.cartasCompradasNesteTurno > 0 && !state.turnoCompraCompleto
  const acaoCartasBloqueiaOutras = fluxoCompraCartasAtivo || state.turnoCompraCompleto
  const baralhoPossivelmenteVazio =
    gameState?.cartas_fechadas_disponiveis === 0 ||
    gameState?.pode_comprar_carta_fechada === false

  /**
   * Reset do turno de compra quando muda o jogador
   */
  useEffect(() => {
    const jogadorAtualStateId = gameState?.jogador_atual_id || null

    if (jogadorAtualStateId && jogadorAtualStateId !== jogadorAtualAnteriorRef.current) {
      dispatch({ type: 'RESET_TURNO' })
    }

    jogadorAtualAnteriorRef.current = jogadorAtualStateId
  }, [gameState?.jogador_atual_id])

  /**
   * Reset manual do turno de compra
   */
  const resetTurnoCompra = useCallback(() => {
    dispatch({ type: 'RESET_TURNO' })
  }, [])

  /**
   * Compra carta do baralho fechado
   */
  const comprarCartaFechada = useCallback(async () => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview) {
      setMensagem("⚠️ Conclua a escolha de bilhetes antes de realizar outra ação.")
      return
    }

    if (!jogadorAtualId) {
      setMensagem("Selecione seu jogador para continuar.")
      return
    }

    if (baralhoPossivelmenteVazio) {
      setMensagem("⚠️ Baralho esgotado: aguarde reposição para comprar cartas fechadas.")
      dispatch({ type: 'BLOQUEIO_BARALHO_VAZIO' })
      return
    }

    const gameId = storageService.getGameId()
    if (!gameId) return

    try {
      const data = await gameApi.drawClosedCard(gameId, jogadorAtualId)
      const cartaComprada = data.card
      const ehLocomotivaFechada = cartaComprada?.eh_locomotiva === true
      const turnoFinalizado = data.turn_completed === true

      setMensagem(`✅ ${data.message}`)

      dispatch({
        type: 'COMPRA_CARTA_FECHADA_SUCESSO',
        ehLocomotiva: ehLocomotivaFechada,
        turnoFinalizado
      })

      // Atualiza mão local imediatamente (otimista) para refletir a compra
      if (cartaComprada) {
        setMinhasCartas((prev) => [
          ...prev,
          normalizarCarta(cartaComprada)
        ])
      }

      await buscarEstadoJogo(gameId)

      if (turnoFinalizado) {
        await handleTurnComplete(buscarEstadoJogo, setMensagem, gameId, data.next_player, 500)
        dispatch({ type: 'RESET_TURNO' })
      }
    } catch (error) {
      // Usa extractErrorMessage para tratamento consistente de erros da API
      const mensagem = extractErrorMessage(error, MENSAGENS.ERRO_CONEXAO)
      setMensagem(`❌ ${mensagem}`)
      dispatch({ type: 'ERRO', mensagem })
    }
  }, [
    fluxoBilhetesAtivo,
    carregandoBilhetesPreview,
    baralhoPossivelmenteVazio,
    jogadorAtualId,
    buscarEstadoJogo,
    setMensagem,
    setMinhasCartas
  ])

  /**
   * Compra carta visível (aberta)
   */
  const comprarCartaAberta = useCallback(async (index: number) => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview) {
      setMensagem("⚠️ Finalize a seleção de bilhetes para seguir com outras ações.")
      return
    }

    if (!jogadorAtualId) {
      setMensagem("Selecione seu jogador para continuar.")
      return
    }

    const gameId = storageService.getGameId()
    if (!gameId || state.turnoCompraCompleto) return

    const cartaSelecionada = gameState?.cartas_visiveis?.[index]
    const ehLocomotivaSelecionada = cartaSelecionada
      ? cartaSelecionada.eh_locomotiva === true || cartaSelecionada.cor?.toLowerCase() === "locomotiva"
      : false

    if (state.bloquearLocomotivaAberta && ehLocomotivaSelecionada) {
      dispatch({ type: 'BLOQUEIO_LOCOMOTIVA' })
      return
    }

    if (!cartaSelecionada) {
      dispatch({ type: 'SET_MENSAGEM', mensagem: MENSAGENS.CARTA_INDISPONIVEL })
      return
    }

    try {
      const data = await gameApi.drawOpenCard(gameId, jogadorAtualId, index)
      const cartaComprada = data.card
      const ehLocomotivaAberta = cartaComprada?.eh_locomotiva === true
      const turnoFinalizado = ehLocomotivaAberta || data.turn_completed === true

      setMensagem(`✅ ${data.message}`)

      dispatch({
        type: 'COMPRA_CARTA_ABERTA_SUCESSO',
        ehLocomotiva: ehLocomotivaAberta,
        turnoFinalizado
      })

      if (cartaComprada) {
        setMinhasCartas((prev) => [
          ...prev,
          normalizarCarta(cartaComprada)
        ])
      }

      await buscarEstadoJogo(gameId)

      if (turnoFinalizado) {
        await handleTurnComplete(buscarEstadoJogo, setMensagem, gameId, data.next_player, 500)
        dispatch({ type: 'RESET_TURNO' })
      }
    } catch (error) {
      // Usa extractErrorMessage para tratamento consistente de erros da API
      const mensagem = extractErrorMessage(error, MENSAGENS.ERRO_CONEXAO)
      setMensagem(`❌ ${mensagem}`)
      dispatch({ type: 'ERRO', mensagem })
    }
  }, [
    fluxoBilhetesAtivo,
    carregandoBilhetesPreview,
    state.turnoCompraCompleto,
    state.bloquearLocomotivaAberta,
    gameState?.cartas_visiveis,
    jogadorAtualId,
    buscarEstadoJogo,
    setMensagem,
    setMinhasCartas
  ])

  return {
    cartasCompradasNesteTurno: state.cartasCompradasNesteTurno,
    turnoCompraCompleto: state.turnoCompraCompleto,
    bloquearLocomotivaAberta: state.bloquearLocomotivaAberta,
    mensagemCompraCartas: state.mensagemCompraCartas,
    fluxoCompraCartasAtivo,
    acaoCartasBloqueiaOutras,
    baralhoPossivelmenteVazio,
    comprarCartaFechada,
    comprarCartaAberta,
    resetTurnoCompra
  }
}
