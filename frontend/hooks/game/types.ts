/**
 * Tipos compartilhados entre os hooks de jogo
 * 
 * Este arquivo define interfaces e tipos usados por múltiplos hooks,
 * evitando dependências cíclicas.
 */

import type { CartaVagao, BilheteDestino, Rota, GameState, CorJogador, JogadorId } from "@/types/game"

// ============================================
// TIPOS DE PONTUAÇÃO
// ============================================

export interface BilheteResumo {
  origem: string
  destino: string
  pontos: number
  completo: boolean
}

export interface PontuacaoFinalResumo {
  jogadorId: JogadorId
  jogadorNome: string
  jogadorCor: CorJogador
  pontosRotas: number
  bilhetesCompletos: BilheteResumo[]
  bilhetesIncompletos: BilheteResumo[]
  pontosBilhetesPositivos: number
  pontosBilhetesNegativos: number
  bonusMaiorCaminho: boolean
  pontosMaiorCaminho: number
  pontuacaoTotal: number
  tamanhoMaiorCaminho?: number
}

// ============================================
// TIPOS DE RESULTADO DE HOOKS
// ============================================

export interface UseGamePollingReturn {
  gameState: GameState | null
  carregando: boolean
  buscarEstadoJogo: (gameId: string) => Promise<void>
  limparDadosJogo: () => void
}

export interface UsePlayerDataReturn {
  minhasCartas: CartaVagao[]
  meusBilhetes: BilheteDestino[]
  jogadorAtualId: string
  ehMinhaVez: boolean
  setMinhasCartas: React.Dispatch<React.SetStateAction<CartaVagao[]>>
  setMeusBilhetes: React.Dispatch<React.SetStateAction<BilheteDestino[]>>
  setJogadorAtualId: React.Dispatch<React.SetStateAction<string>>
}

export interface UseCardPurchaseReturn {
  cartasCompradasNesteTurno: number
  turnoCompraCompleto: boolean
  bloquearLocomotivaAberta: boolean
  mensagemCompraCartas: string | null
  fluxoCompraCartasAtivo: boolean
  acaoCartasBloqueiaOutras: boolean
  baralhoPossivelmenteVazio: boolean
  comprarCartaFechada: () => Promise<void>
  comprarCartaAberta: (index: number) => Promise<void>
  resetTurnoCompra: () => void
}

export interface UseRouteConquestReturn {
  rotasDoJogo: Rota[]
  rotaSelecionada: string | null
  rotaSelecionadaInfo: Rota | null
  cartasSelecionadas: number[]
  podeConquistarRota: boolean
  conquistarRota: () => Promise<void>
  toggleCartaSelecionada: (indice: number, limite?: number) => void
  handleSelecaoRotaMapa: (rotaId: string | null) => void
  setRotaSelecionada: React.Dispatch<React.SetStateAction<string | null>>
  setCartasSelecionadas: React.Dispatch<React.SetStateAction<number[]>>
  setRotasDoJogo: React.Dispatch<React.SetStateAction<Rota[]>>
}

export interface UseTicketFlowReturn {
  mostrarModalBilhetes: boolean
  bilhetesDisponiveis: BilheteDestino[]
  bilhetesSelecionados: number[]
  fluxoBilhetesAtivo: boolean
  carregandoBilhetesPreview: boolean
  iniciarFluxoBilhetes: () => Promise<void>
  confirmarBilhetes: () => Promise<void>
  toggleBilheteSelecionado: (index: number, minimo?: number) => void
  cancelarFluxoBilhetes: () => void
  setMostrarModalBilhetes: React.Dispatch<React.SetStateAction<boolean>>
  setBilhetesSelecionados: React.Dispatch<React.SetStateAction<number[]>>
}

export interface UseGameEndReturn {
  pontuacaoFinal: PontuacaoFinalResumo[]
  mostrarTelaFimJogo: boolean
  mensagemFimJogo: string | null
  carregarPontuacaoFinal: (gameId?: string) => Promise<void>
  handleVoltarMenu: () => void
  handleJogarNovamente: () => void
}

// ============================================
// TIPOS DE DEPENDÊNCIAS ENTRE HOOKS
// ============================================

export interface CardPurchaseDeps {
  gameState: GameState | null
  jogadorAtualId: string
  fluxoBilhetesAtivo: boolean
  carregandoBilhetesPreview: boolean
  buscarEstadoJogo: (gameId: string) => Promise<void>
  setMensagem: (msg: string) => void
  setMinhasCartas: React.Dispatch<React.SetStateAction<CartaVagao[]>>
}

export interface RouteConquestDeps {
  minhasCartas: CartaVagao[]
  jogadorAtualId: string
  fluxoBilhetesAtivo: boolean
  carregandoBilhetesPreview: boolean
  acaoCartasBloqueiaOutras: boolean
  buscarEstadoJogo: (gameId: string) => Promise<void>
  setMensagem: (msg: string) => void
}

export interface TicketFlowDeps {
  jogadorAtualId: string
  acaoCartasBloqueiaOutras: boolean
  buscarEstadoJogo: (gameId: string) => Promise<void>
  setMensagem: (msg: string) => void
}
