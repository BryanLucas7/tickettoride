/**
 * Tipos de UI - Interfaces específicas para componentes React
 * 
 * Este arquivo centraliza tipos usados exclusivamente em componentes
 * de interface do usuário, separando-os dos tipos de domínio e API.
 * 
 * @module types/ui
 */

import type { CorJogador, CorCartaString, CorRotaString } from './game'

// ============================================
// TIPOS DE CORES
// ============================================

/**
 * Union type de todas as cores válidas no sistema
 * Usado em funções de conversão de cor para CSS
 */
export type CorSistema = CorJogador | CorCartaString | CorRotaString

/**
 * Função getter de cor genérica
 */
export type ColorGetter = (cor: CorSistema | string) => string

/**
 * Interface para funções auxiliares de cor
 * Usada em múltiplos componentes que exibem cartas/cores
 * 
 * @example
 * function MeuComponente({ getCoresBg, getCorTexto }: ColorHelpers) {
 *   return <div className={getCoresBg('vermelho')} />
 * }
 */
export interface ColorHelpers {
  /** Retorna a classe CSS de background para uma cor */
  getCoresBg: ColorGetter
  /** Retorna a classe CSS de texto para uma cor */
  getCorTexto: ColorGetter
  /** Retorna a letra/símbolo representando uma cor */
  getLetraCor: ColorGetter
}

// ============================================
// TIPOS DE PROPS DE COMPONENTES
// ============================================

/**
 * Props base para componentes de jogador
 */
export interface JogadorDisplayProps {
  nome: string
  cor: CorJogador
  pontos?: number
  ehAtual?: boolean
}

/**
 * Props para exibição de contagem de itens
 */
export interface ContadorProps {
  valor: number
  label: string
  icone?: string
}

// ============================================
// TIPOS DE ESTADO DE UI
// ============================================

/**
 * Estado de carregamento genérico
 */
export interface LoadingState {
  isLoading: boolean
  error: string | null
}

/**
 * Estado de modal/dialog
 */
export interface ModalState {
  isOpen: boolean
  title?: string
  content?: string
}

/**
 * Estado de notificação/toast
 */
export interface NotificationState {
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  visible: boolean
}

// ============================================
// TIPOS DE CONFIGURAÇÃO VISUAL
// ============================================

/**
 * Configuração de cores para um jogador
 */
export interface PlayerColorConfig {
  bg: string
  text: string
  border: string
}

/**
 * Coordenadas de posição na tela
 */
export interface Position {
  x: number
  y: number
}

/**
 * Dimensões de elemento
 */
export interface Dimensions {
  width: number
  height: number
}

// ============================================
// TIPOS DE EVENTOS DE UI
// ============================================

/**
 * Callback de seleção genérico
 */
export type SelectionCallback<T> = (item: T) => void

/**
 * Callback de ação sem parâmetros
 */
export type ActionCallback = () => void

/**
 * Callback de ação assíncrona
 */
export type AsyncActionCallback = () => Promise<void>

// ============================================
// TIPOS DE FORMULÁRIO
// ============================================

/**
 * Estado de campo de formulário
 */
export interface FormFieldState<T = string> {
  value: T
  error: string | null
  touched: boolean
}

/**
 * Resultado de validação de formulário
 */
export interface FormValidationResult {
  isValid: boolean
  errors: Record<string, string>
}
