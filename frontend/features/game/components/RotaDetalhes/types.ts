/**
 * Tipos compartilhados para RotaDetalhes
 */

import type { UseGameEngineReturn } from "@/hooks/useGameEngine"

// ============================================
// TIPOS BASE
// ============================================

export interface RotaMapa {
  comprimento: number
  cor: string
}

export interface RotaDoJogo {
  conquistada?: boolean
  proprietario_nome?: string | null
}

// ============================================
// FUNÇÕES DE COR (CALLBACKS)
// ============================================

export interface ColorHelpers {
  getCoresBg: (cor: string) => string
  getCorTexto: (cor: string) => string
  getLetraCor: (cor: string) => string
}

// ============================================
// PROPS DOS COMPONENTES
// ============================================

export interface RotaDetalhesPanelProps extends ColorHelpers {
  rotaMapa: RotaMapa
  rotaDoJogo: RotaDoJogo | null | undefined
  game: UseGameEngineReturn
  ehMinhaVez: boolean
}

export interface RotaConquistadaProps {
  proprietarioNome: string | null | undefined
}

export interface RotaBloqueadaProps {
  motivo: 'cartas' | 'bilhetes'
}

// RotaSelecaoCartas agora usa useCardColors internamente (via CardSelectionGrid)
// então não precisa mais receber ColorHelpers
export interface RotaSelecaoCartasProps {
  rotaMapa: RotaMapa
  game: UseGameEngineReturn
}
