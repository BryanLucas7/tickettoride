/**
 * useGameEngine - Hook compositor para gerenciamento do jogo
 * 
 * Este hook segue o padrão Facade, orquestrando múltiplos hooks
 * especializados e expondo uma interface unificada para o componente.
 * 
 * Responsabilidade: Composição e orquestração (não lógica de negócio)
 * 
 * Hooks compostos:
 * - useGamePolling: Sincronização com backend
 * - usePlayerData: Dados do jogador (cartas, bilhetes)
 * - useCardPurchase: Fluxo de compra de cartas
 * - useRouteConquest: Conquista de rotas
 * - useTicketFlow: Compra de bilhetes
 * - useGameEnd: Fim de jogo e pontuação
 * 
 * DRY: Tipos reutilizados de ./game/types para evitar duplicação
 */

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import type { GameState, Jogador, Rota } from "@/types/game"
import { gameApi } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import {
  useGamePolling,
  usePlayerData,
  useCardPurchase,
  useRouteConquest,
  useTicketFlow,
  useGameEnd,
  type PontuacaoFinalResumo,
  type UseTicketFlowReturn,
  type UseCardPurchaseReturn,
  type UseRouteConquestReturn,
  type UseGameEndReturn
} from "./game"

/**
 * Interface completa retornada pelo useGameEngine
 * 
 * DRY: Usa Pick para reutilizar tipos dos hooks especializados
 * ao invés de redefinir cada propriedade manualmente.
 */
export interface UseGameEngineReturn {
  // Estado do jogo
  gameState: GameState | null
  carregando: boolean
  mensagem: string
  
  // Dados do jogador
  minhasCartas: ReturnType<typeof usePlayerData>["minhasCartas"]
  meusBilhetes: ReturnType<typeof usePlayerData>["meusBilhetes"]
  jogadorAtualId: string
  ehMinhaVez: boolean
  
  // Rotas
  rotasDoJogo: Rota[]
  rotaSelecionada: string | null
  rotaSelecionadaInfo: Rota | null
  cartasSelecionadas: number[]
  podeConquistarRota: boolean
  
  // Compra de cartas
  cartasCompradasNesteTurno: number
  turnoCompraCompleto: boolean
  bloquearLocomotivaAberta: boolean
  mensagemCompraCartas: string | null
  fluxoCompraCartasAtivo: boolean
  acaoCartasBloqueiaOutras: boolean
  baralhoPossivelmenteVazio: boolean
  
  // Bilhetes
  mostrarModalBilhetes: boolean
  bilhetesDisponiveis: ReturnType<typeof useTicketFlow>["bilhetesDisponiveis"]
  bilhetesSelecionados: number[]
  fluxoBilhetesAtivo: boolean
  carregandoBilhetesPreview: boolean
  
  // Fim de jogo
  pontuacaoFinal: PontuacaoFinalResumo[]
  mostrarTelaFimJogo: boolean
  mensagemFimJogo: string | null
  
  // Ações de cartas
  comprarCartaFechada: () => Promise<void>
  comprarCartaAberta: (index: number) => Promise<void>
  
  // Ações de rotas
  conquistarRota: () => Promise<void>
  toggleCartaSelecionada: (indice: number, limite?: number) => void
  handleSelecaoRotaMapa: (rotaId: string | null) => void
  setCartasSelecionadas: React.Dispatch<React.SetStateAction<number[]>>
  setRotaSelecionada: React.Dispatch<React.SetStateAction<string | null>>
  
  // Ações de bilhetes
  iniciarFluxoBilhetes: () => Promise<void>
  confirmarBilhetes: () => Promise<void>
  toggleBilheteSelecionado: (index: number, minimo?: number) => void
  cancelarFluxoBilhetes: () => void
  setMostrarModalBilhetes: React.Dispatch<React.SetStateAction<boolean>>
  setBilhetesSelecionados: React.Dispatch<React.SetStateAction<number[]>>
  
  // Navegação
  handleVoltarMenu: () => void
  handleJogarNovamente: () => void
  
  // Utilitários
  setMensagem: (msg: string) => void
  buscarEstadoJogo: (gameId: string) => Promise<void>
}

/**
 * Hook compositor principal
 */
export function useGameEngine(): UseGameEngineReturn {
  const router = useRouter()
  
  // Estado de mensagem (UI feedback)
  const [mensagem, setMensagem] = useState("")
  
  // Hook de polling (estado base do jogo)
  const polling = useGamePolling()
  const { gameState, carregando, buscarEstadoJogo, limparDadosJogo } = polling
  
  // Hook de dados do jogador
  const playerData = usePlayerData({
    gameState,
    limparDadosJogo,
    onInvalidData: () => {
      storageService.removeCurrentPlayer()
      setMensagem("Selecione seu jogador para continuar.")
      router.push("/entrar")
    }
  })
  
  // Hook de bilhetes (precisa ser declarado antes de cardPurchase)
  const ticketFlow = useTicketFlow({
    jogadorAtualId: playerData.jogadorAtualId,
    acaoCartasBloqueiaOutras: false, // Será atualizado após cardPurchase
    buscarEstadoJogo,
    setMensagem
  })
  
  // Hook de compra de cartas
  const cardPurchase = useCardPurchase({
    gameState,
    jogadorAtualId: playerData.jogadorAtualId,
    fluxoBilhetesAtivo: ticketFlow.fluxoBilhetesAtivo,
    carregandoBilhetesPreview: ticketFlow.carregandoBilhetesPreview,
    buscarEstadoJogo,
    setMensagem,
    setMinhasCartas: playerData.setMinhasCartas
  })
  
  // Hook de conquista de rotas
  const routeConquest = useRouteConquest({
    minhasCartas: playerData.minhasCartas,
    jogadorAtualId: playerData.jogadorAtualId,
    fluxoBilhetesAtivo: ticketFlow.fluxoBilhetesAtivo,
    carregandoBilhetesPreview: ticketFlow.carregandoBilhetesPreview,
    acaoCartasBloqueiaOutras: cardPurchase.acaoCartasBloqueiaOutras,
    buscarEstadoJogo,
    setMensagem
  })
  
  // Hook de fim de jogo
  const gameEnd = useGameEnd({
    gameState,
    limparDadosJogo
  })
  
  // Busca rotas quando gameState muda
  useEffect(() => {
    const fetchRoutes = async () => {
      const gameId = storageService.getGameId()
      if (!gameId || !gameState) return
      
      try {
        const rotasData = await gameApi.getRoutes(gameId)
        if (rotasData.routes && Array.isArray(rotasData.routes)) {
          routeConquest.setRotasDoJogo(rotasData.routes)
        }
      } catch (error) {
        console.error("Erro ao buscar rotas:", error)
      }
    }
    
      fetchRoutes()
  }, [gameState?.jogador_atual_id, gameState?.finalizado, routeConquest.setRotasDoJogo])
  
  // Atualiza mensagem baseada no estado do jogo
  useEffect(() => {
    if (!gameState) return
    
    if (gameState.finalizado) {
      setMensagem("🏁 Jogo finalizado! Aguarde os resultados finais.")
    } else {
      const jogadorDaVez = gameState.jogadores.find(
        (j: Jogador) => j.id === gameState.jogador_atual_id
      )
      setMensagem(
        jogadorDaVez 
          ? `🎮 Vez de: ${jogadorDaVez.nome}` 
          : "🎮 Aguardando..."
      )
    }
  }, [gameState?.jogador_atual_id, gameState?.finalizado])
  
  // Mensagem inicial quando não há jogo
  useEffect(() => {
    if (!carregando && !gameState) {
      setMensagem("Nenhum jogo ativo. Crie um jogo na tela de configuração.")
    }
  }, [carregando, gameState])
  
  return {
    // Estado do jogo
    gameState,
    carregando,
    mensagem,
    
    // Dados do jogador
    minhasCartas: playerData.minhasCartas,
    meusBilhetes: playerData.meusBilhetes,
    jogadorAtualId: playerData.jogadorAtualId,
    ehMinhaVez: playerData.ehMinhaVez,
    
    // Rotas
    rotasDoJogo: routeConquest.rotasDoJogo,
    rotaSelecionada: routeConquest.rotaSelecionada,
    rotaSelecionadaInfo: routeConquest.rotaSelecionadaInfo,
    cartasSelecionadas: routeConquest.cartasSelecionadas,
    podeConquistarRota: routeConquest.podeConquistarRota,
    
    // Compra de cartas
    cartasCompradasNesteTurno: cardPurchase.cartasCompradasNesteTurno,
    turnoCompraCompleto: cardPurchase.turnoCompraCompleto,
    bloquearLocomotivaAberta: cardPurchase.bloquearLocomotivaAberta,
    mensagemCompraCartas: cardPurchase.mensagemCompraCartas,
    fluxoCompraCartasAtivo: cardPurchase.fluxoCompraCartasAtivo,
    acaoCartasBloqueiaOutras: cardPurchase.acaoCartasBloqueiaOutras,
    baralhoPossivelmenteVazio: cardPurchase.baralhoPossivelmenteVazio,
    
    // Bilhetes
    mostrarModalBilhetes: ticketFlow.mostrarModalBilhetes,
    bilhetesDisponiveis: ticketFlow.bilhetesDisponiveis,
    bilhetesSelecionados: ticketFlow.bilhetesSelecionados,
    fluxoBilhetesAtivo: ticketFlow.fluxoBilhetesAtivo,
    carregandoBilhetesPreview: ticketFlow.carregandoBilhetesPreview,
    
    // Fim de jogo
    pontuacaoFinal: gameEnd.pontuacaoFinal,
    mostrarTelaFimJogo: gameEnd.mostrarTelaFimJogo,
    mensagemFimJogo: gameEnd.mensagemFimJogo,
    
    // Ações de cartas
    comprarCartaFechada: cardPurchase.comprarCartaFechada,
    comprarCartaAberta: cardPurchase.comprarCartaAberta,
    
    // Ações de rotas
    conquistarRota: routeConquest.conquistarRota,
    toggleCartaSelecionada: routeConquest.toggleCartaSelecionada,
    handleSelecaoRotaMapa: routeConquest.handleSelecaoRotaMapa,
    setCartasSelecionadas: routeConquest.setCartasSelecionadas,
    setRotaSelecionada: routeConquest.setRotaSelecionada,
    
    // Ações de bilhetes
    iniciarFluxoBilhetes: ticketFlow.iniciarFluxoBilhetes,
    confirmarBilhetes: ticketFlow.confirmarBilhetes,
    toggleBilheteSelecionado: ticketFlow.toggleBilheteSelecionado,
    cancelarFluxoBilhetes: ticketFlow.cancelarFluxoBilhetes,
    setMostrarModalBilhetes: ticketFlow.setMostrarModalBilhetes,
    setBilhetesSelecionados: ticketFlow.setBilhetesSelecionados,
    
    // Navegação
    handleVoltarMenu: gameEnd.handleVoltarMenu,
    handleJogarNovamente: gameEnd.handleJogarNovamente,
    
    // Utilitários
    setMensagem,
    buscarEstadoJogo
  }
}
