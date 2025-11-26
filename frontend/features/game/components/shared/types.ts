/**
 * Tipos Compartilhados para Componentes do Jogo
 * 
 * Este arquivo centraliza tipos usados em múltiplos componentes
 * do módulo features/game/components.
 * 
 * CONVENÇÕES:
 * - Importar tipos de domínio de @/types/game
 * - Importar tipos de UI de @/types/ui
 * - Definir aqui apenas tipos específicos de componentes compartilhados
 * 
 * @module features/game/components/shared/types
 */

import type { UseGameEngineReturn } from "@/hooks/useGameEngine"
import type { GameState, CartaVagao, CorJogador, CorRotaString, JogadorId, RotaId, BilheteId } from "@/types/game"
import type { ColorHelpers } from "@/types/ui"

// ============================================
// RE-EXPORTS PARA CONVENIÊNCIA
// ============================================

export type { UseGameEngineReturn } from "@/hooks/useGameEngine"
export type { GameState, CartaVagao, Rota, BilheteDestino } from "@/types/game"
export type { ColorHelpers } from "@/types/ui"

// ============================================
// PROPS COMUNS PARA PAINÉIS DE JOGO
// ============================================

/**
 * Props base para componentes que usam o game engine
 */
export interface GameEngineProps {
  game: UseGameEngineReturn
}

/**
 * Props para componentes que precisam do estado do jogo
 */
export interface GameStateProps {
  gameState: GameState | null
}

/**
 * Props para componentes que indicam vez do jogador
 */
export interface TurnoProps {
  ehMinhaVez: boolean
}

/**
 * Props combinadas para ações do turno
 */
export interface AcoesBaseProps extends GameEngineProps, ColorHelpers {
  gameState: GameState | null
}

// ============================================
// TIPOS PARA CARTAS
// ============================================

/**
 * Props para componentes que exibem cartas visíveis
 */
export interface CartasVisivelProps extends ColorHelpers {
  cartas: CartaVagao[]
  onComprar?: (index: number) => void
  desabilitada?: (index: number) => boolean
}

/**
 * Carta com informação de seleção
 */
export interface CartaSelecionavel extends CartaVagao {
  selecionada: boolean
  indice: number
}

// ============================================
// TIPOS PARA JOGADORES
// ============================================

/**
 * Informação básica de jogador para exibição
 */
export interface JogadorDisplay {
  id: JogadorId
  nome: string
  cor: CorJogador
  pontos: number
  trens_disponiveis: number
  ehAtual: boolean
}

/**
 * Jogador em formato de ranking/placar
 */
export interface JogadorPlacar {
  id: JogadorId
  nome: string
  cor: CorJogador
  pontos: number
  posicao?: number
}

// ============================================
// TIPOS PARA ROTAS
// ============================================

/**
 * Informações de rota do mapa (estáticas)
 */
export interface RotaMapa {
  id: RotaId
  cidadeA: string
  cidadeB: string
  comprimento: number
  cor: CorRotaString
}

/**
 * Informações de rota em jogo (dinâmicas)
 */
export interface RotaDoJogo {
  id: RotaId
  conquistada: boolean
  proprietario_id: JogadorId | null
  proprietario_nome: string | null
  proprietario_cor: CorJogador | null
}

/**
 * Rota conquistada para exibição
 */
export interface RotaConquistadaDisplay {
  id: RotaId
  origem: string
  destino: string
  comprimento: number
  pontos: number
}

// ============================================
// TIPOS PARA BILHETES
// ============================================

/**
 * Bilhete de destino para exibição em UI
 */
export interface BilheteUI {
  id: BilheteId
  origem: string
  destino: string
  pontos: number
  completo: boolean
}

/**
 * Estatísticas de bilhetes
 */
export interface BilhetesStats {
  totalBilhetes: number
  bilhetesCompletos: number
  bilhetesPendentes: number
  pontosGanhos: number
  pontosPerdidos: number
  pontosLiquidos: number
}

// ============================================
// TIPOS PARA MENSAGENS/FEEDBACK
// ============================================

/**
 * Tipo de mensagem de feedback
 */
export type TipoMensagem = 'success' | 'error' | 'warning' | 'info'

/**
 * Mensagem de feedback para o usuário
 */
export interface Mensagem {
  texto: string
  tipo: TipoMensagem
  visivel: boolean
}

// ============================================
// TIPOS PARA MODAIS
// ============================================

/**
 * Props base para modais
 */
export interface ModalBaseProps {
  exibir: boolean
  onFechar?: () => void
}

/**
 * Props para modal de confirmação
 */
export interface ModalConfirmacaoProps extends ModalBaseProps {
  titulo: string
  mensagem: string
  onConfirmar: () => void
  textoBotaoConfirmar?: string
  textoBotaoCancelar?: string
}
