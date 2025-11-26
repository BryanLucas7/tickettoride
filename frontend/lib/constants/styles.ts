/**
 * UI Style Constants - Constantes centralizadas para estilos de UI
 * 
 * REFATORAÇÃO DRY: Centraliza estilos de botões que estavam
 * duplicados em 5+ componentes.
 * 
 * Benefícios:
 * - Consistência visual garantida
 * - Facilita mudanças globais de estilo
 * - Reduz erro humano em copy/paste
 * - Melhora manutenibilidade
 */

// ============================================
// ESTILOS DE BOTÃO
// ============================================

/**
 * Classes Tailwind para estado disabled de botões
 */
export const DISABLED_STYLES = {
  /** Estilo padrão para botões desabilitados */
  DEFAULT: 'disabled:bg-gray-300 disabled:text-gray-600',
  /** Estilo com cursor not-allowed */
  WITH_CURSOR: 'disabled:bg-gray-300 disabled:text-gray-600 disabled:cursor-not-allowed'
} as const

/**
 * Estilos base de botão com variantes de cor
 */
export const BUTTON_BASE = 'font-semibold rounded-lg transition-colors' as const

/**
 * Estilos completos de botões por cor/variante
 */
export const BUTTON_STYLES = {
  /** Botão verde (compra de cartas, confirmar) */
  GREEN: `bg-green-600 hover:bg-green-700 text-white ${BUTTON_BASE} ${DISABLED_STYLES.WITH_CURSOR}`,
  
  /** Botão laranja (bilhetes) */
  ORANGE: `bg-orange-600 hover:bg-orange-700 text-white ${BUTTON_BASE} ${DISABLED_STYLES.WITH_CURSOR}`,
  
  /** Botão roxo (conquista de rotas) */
  PURPLE: `bg-purple-600 hover:bg-purple-700 text-white ${BUTTON_BASE} ${DISABLED_STYLES.DEFAULT}`,
  
  /** Botão azul (ações primárias) */
  BLUE: `bg-blue-600 hover:bg-blue-700 text-white ${BUTTON_BASE} ${DISABLED_STYLES.DEFAULT}`,
  
  /** Botão vermelho (cancelar, deletar) */
  RED: `bg-red-600 hover:bg-red-700 text-white ${BUTTON_BASE} ${DISABLED_STYLES.DEFAULT}`,
  
  /** Botão cinza (ação secundária) */
  GRAY: `bg-gray-600 hover:bg-gray-700 text-white ${BUTTON_BASE} ${DISABLED_STYLES.DEFAULT}`,
} as const

/**
 * Tamanhos de botão
 */
export const BUTTON_SIZES = {
  /** Tamanho pequeno: py-1 px-2 text-xs */
  SM: 'py-1 px-2 text-xs',
  /** Tamanho médio (padrão): py-2 px-4 text-sm */
  MD: 'py-2 px-4 text-sm',
  /** Tamanho grande: py-3 px-4 text-base */
  LG: 'py-3 px-4 text-base',
} as const

/**
 * Combina estilo de botão com tamanho
 * 
 * @example
 * ```tsx
 * <button className={getButtonClass('GREEN', 'MD')}>
 *   Confirmar
 * </button>
 * ```
 */
export function getButtonClass(
  color: keyof typeof BUTTON_STYLES,
  size: keyof typeof BUTTON_SIZES = 'MD'
): string {
  return `${BUTTON_STYLES[color]} ${BUTTON_SIZES[size]}`
}

/**
 * Combina classes de botão com classes customizadas
 * 
 * @example
 * ```tsx
 * <button className={buttonClass('PURPLE', 'MD', 'flex-1 min-w-[180px]')}>
 *   Conquistar Rota
 * </button>
 * ```
 */
export function buttonClass(
  color: keyof typeof BUTTON_STYLES,
  size: keyof typeof BUTTON_SIZES = 'MD',
  customClasses?: string
): string {
  const base = getButtonClass(color, size)
  return customClasses ? `${customClasses} ${base}` : base
}

// ============================================
// ESTILOS DE CARD/PAINEL
// ============================================

/**
 * Estilos de painel/card
 */
export const PANEL_STYLES = {
  /** Painel padrão com fundo escuro */
  DARK: 'bg-gray-800 rounded-lg p-4',
  /** Painel com borda */
  BORDERED: 'bg-gray-800 rounded-lg p-4 border border-gray-700',
  /** Painel com sombra */
  ELEVATED: 'bg-gray-800 rounded-lg p-4 shadow-lg',
} as const

// ============================================
// ESTILOS DE TEXTO
// ============================================

/**
 * Estilos de texto por tamanho/importância
 */
export const TEXT_STYLES = {
  /** Título de seção */
  SECTION_TITLE: 'text-lg font-bold text-white mb-2',
  /** Label de campo */
  LABEL: 'text-sm font-medium text-gray-300',
  /** Texto secundário/descrição */
  MUTED: 'text-sm text-gray-400',
  /** Texto de erro */
  ERROR: 'text-sm text-red-400',
  /** Texto de sucesso */
  SUCCESS: 'text-sm text-green-400',
} as const
