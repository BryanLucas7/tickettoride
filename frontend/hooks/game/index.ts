/**
 * Barrel export para os hooks de jogo
 */

export { useGamePolling } from "./useGamePolling"
export { usePlayerData } from "./usePlayerData"
export { useCardPurchase } from "./useCardPurchase"
export { useRouteConquest } from "./useRouteConquest"
export { useTicketFlow } from "./useTicketFlow"
export { useGameEnd } from "./useGameEnd"

// Re-export tipos para evitar duplicação (DRY)
export type { 
  PontuacaoFinalResumo,
  UseTicketFlowReturn,
  UseCardPurchaseReturn,
  UseRouteConquestReturn,
  UseGameEndReturn
} from "./types"
