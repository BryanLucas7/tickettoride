/**
 * Tipos compartilhados para AcoesDoTurno
 */

import type { GameState } from "@/types/game"
import type { UseGameEngineReturn } from "@/hooks/useGameEngine"

/**
 * Props do componente principal AcoesDoTurno
 */
export interface AcoesDoTurnoProps {
    game: UseGameEngineReturn
    gameState: GameState
    cartasCompradasNoTurno: number
    cartasFechadasRestantes: number | null
    getCoresBg: (cor: string) => string
    getCorTexto: (cor: string) => string
    getLetraCor: (cor: string) => string
}

/**
 * Props da seção de compra de cartas
 */
export interface SecaoCompraCartasProps {
    game: UseGameEngineReturn
    gameState: GameState
    cartasCompradasNoTurno: number
    cartasFechadasRestantes: number | null
    getCoresBg: (cor: string) => string
    getCorTexto: (cor: string) => string
    getLetraCor: (cor: string) => string
}

/**
 * Props do botão de carta visível
 */
export interface CartaVisivelButtonProps {
    carta: {
        cor: string
        eh_locomotiva?: boolean
    }
    index: number
    desabilitada: boolean
    bloqueadaLocomotiva: boolean
    turnoCompraCompleto: boolean
    titulo: string
    onClick: () => void
    getCoresBg: (cor: string) => string
    getCorTexto: (cor: string) => string
    getLetraCor: (cor: string) => string
}

/**
 * Props da seção de compra de bilhetes
 */
export interface SecaoCompraBilhetesProps {
    game: UseGameEngineReturn
}

/**
 * Props do componente de mensagem de feedback
 */
export interface MensagemFeedbackProps {
    mensagem: string | null
    tipo?: 'warning' | 'error' | 'info'
}
