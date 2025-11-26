/**
 * useRouteConquest - Hook para conquista de rotas
 * 
 * Responsabilidade única: Gerenciar seleção de rotas, seleção de cartas
 * e o processo de conquista de rotas.
 * 
 * DRY REFACTORING: Usa useToggleSelection para lógica de seleção
 */

import { useState, useEffect, useCallback } from "react"
import type { CartaVagao, Rota, GameState } from "@/types/game"
import { gameApi } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import { useToggleSelection } from "@/hooks/useToggleSelection"
import { validarSelecaoCartasParaRota } from "@/lib/gameRules"
import type { UseRouteConquestReturn, RouteConquestDeps } from "./types"
import { handleTurnComplete, handleApiError } from "./utils"

export function useRouteConquest(deps: RouteConquestDeps): UseRouteConquestReturn {
  const {
    minhasCartas,
    jogadorAtualId,
    fluxoBilhetesAtivo,
    carregandoBilhetesPreview,
    acaoCartasBloqueiaOutras,
    buscarEstadoJogo,
    setMensagem
  } = deps
  
  const [rotasDoJogo, setRotasDoJogo] = useState<Rota[]>([])
  const [rotaSelecionada, setRotaSelecionada] = useState<string | null>(null)
  
  // Informações da rota selecionada
  const rotaSelecionadaInfo = rotaSelecionada
    ? rotasDoJogo.find((rota) => rota.id === rotaSelecionada) ?? null
    : null
  
  // Usa hook de seleção toggle (limite máximo baseado no comprimento da rota)
  const {
    selected: cartasSelecionadas,
    toggle: toggleCartaInternal,
    reset: resetCartas,
    setSelected: setCartasSelecionadas
  } = useToggleSelection<number>({ max: rotaSelecionadaInfo?.comprimento })
  
  // Mapeia índices para cartas
  const cartasSelecionadasDetalhes = cartasSelecionadas
    .map((indice) => minhasCartas[indice])
    .filter((carta): carta is CartaVagao => Boolean(carta))
  
  // Validação da seleção atual
  const validacaoSelecaoAtual = validarSelecaoCartasParaRota(rotaSelecionadaInfo, cartasSelecionadasDetalhes)
  const indicesValidos = cartasSelecionadasDetalhes.length === cartasSelecionadas.length
  
  const podeConquistarRota =
    validacaoSelecaoAtual.valida &&
    indicesValidos &&
    !fluxoBilhetesAtivo &&
    !carregandoBilhetesPreview &&
    !acaoCartasBloqueiaOutras
  
  /**
   * Reset cartas selecionadas ao mudar rota
   */
  useEffect(() => {
    resetCartas()
  }, [rotaSelecionada, resetCartas])
  
  /**
   * Toggle seleção de carta (wrapper para manter compatibilidade)
   */
  const toggleCartaSelecionada = useCallback((indice: number, limite?: number) => {
    // O limite agora é passado como override para o toggle
    toggleCartaInternal(indice, limite)
  }, [toggleCartaInternal])
  
  /**
   * Handler para seleção de rota no mapa
   */
  const handleSelecaoRotaMapa = useCallback((rotaId: string | null) => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview || acaoCartasBloqueiaOutras) {
      setMensagem(
        acaoCartasBloqueiaOutras
          ? "⚠️ Conclua a compra de cartas antes de selecionar rotas."
          : "⚠️ Termine a compra de bilhetes antes de selecionar rotas."
      )
      return
    }

    if (!rotaId) {
      setRotaSelecionada(null)
      return
    }

    const rotaInfo = rotasDoJogo.find((rota) => rota.id === rotaId)

    if (rotaInfo?.conquistada) {
      setMensagem("⚠️ Essa rota já foi conquistada por outro jogador.")
      setRotaSelecionada(null)
      return
    }

    setRotaSelecionada(rotaId)
  }, [fluxoBilhetesAtivo, carregandoBilhetesPreview, acaoCartasBloqueiaOutras, rotasDoJogo, setMensagem])
  
  /**
   * Conquistar a rota selecionada
   */
  const conquistarRota = useCallback(async () => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview || acaoCartasBloqueiaOutras) {
      setMensagem(
        acaoCartasBloqueiaOutras
          ? "⚠️ Você escolheu comprar cartas neste turno. Finalize essa ação antes de conquistar rotas."
          : "⚠️ Termine a compra de bilhetes antes de conquistar rotas."
      )
      return
    }

    if (!rotaSelecionada) {
      setMensagem("❌ Selecione uma rota disponível no mapa antes de conquistar")
      return
    }

    if (cartasSelecionadas.length === 0) {
      setMensagem("❌ Escolha as cartas que serão usadas na conquista da rota")
      return
    }

    if (!rotaSelecionadaInfo) {
      setMensagem("❌ Rota selecionada não encontrada. Atualize o estado do jogo.")
      return
    }

    if (!jogadorAtualId) {
      setMensagem("Selecione seu jogador para continuar.")
      return
    }
    
    if (rotaSelecionadaInfo.conquistada) {
      setMensagem("❌ Essa rota já foi conquistada.")
      return
    }

    // Valida seleção
    const validacaoSelecao = validarSelecaoCartasParaRota(rotaSelecionadaInfo, cartasSelecionadasDetalhes)

    if (!validacaoSelecao.valida || !validacaoSelecao.cartasDetalhes) {
      setMensagem(validacaoSelecao.mensagem ?? "❌ Seleção de cartas inválida para esta rota.")
      return
    }

    const cartasDetalhes = validacaoSelecao.cartasDetalhes

    // As cores já são CorCartaString (tipadas corretamente)
    const cartasParaEnviar = cartasDetalhes
      .map((carta) => carta.cor.toLowerCase())

    if (cartasParaEnviar.length !== cartasSelecionadas.length) {
      setMensagem("❌ Não foi possível localizar todas as cartas selecionadas. Atualize as cartas e tente novamente.")
      return
    }

    try {
      const gameId = storageService.getGameId()
      if (!gameId) {
        setMensagem("❌ Jogo não encontrado. Recarregue a página.")
        return
      }

      const cartasFormatadas = cartasDetalhes.map((carta) => ({
        cor: carta.cor.toLowerCase(),
        eh_locomotiva: carta.eh_locomotiva
      }))
      
      const data = await gameApi.conquerRoute(gameId, jogadorAtualId, rotaSelecionada, cartasFormatadas)

      if (data.success) {
        setMensagem(`✅ ${data.message} (+${data.points} pontos)`)
        setRotaSelecionada(null)
        resetCartas()
        
        await handleTurnComplete(buscarEstadoJogo, setMensagem, gameId, data.next_player, 2000)
      } else {
        setMensagem(`❌ ${data.message || "Não foi possível conquistar a rota"}`)
      }
    } catch (error) {
      handleApiError(error, setMensagem, "Erro ao conquistar rota")
    }
  }, [
    fluxoBilhetesAtivo,
    carregandoBilhetesPreview,
    acaoCartasBloqueiaOutras,
    rotaSelecionada,
    cartasSelecionadas,
    rotaSelecionadaInfo,
    cartasSelecionadasDetalhes,
    jogadorAtualId,
    buscarEstadoJogo,
    setMensagem,
    resetCartas
  ])
  
  return {
    rotasDoJogo,
    rotaSelecionada,
    rotaSelecionadaInfo,
    cartasSelecionadas,
    podeConquistarRota,
    conquistarRota,
    toggleCartaSelecionada,
    handleSelecaoRotaMapa,
    setRotaSelecionada,
    setCartasSelecionadas,
    setRotasDoJogo
  }
}
