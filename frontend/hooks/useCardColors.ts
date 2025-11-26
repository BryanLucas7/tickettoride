/**
 * useCardColors - Hook para cores de cartas de vagão
 * 
 * REFATORAÇÃO DRY: Elimina prop drilling de getCoresBg, getCorTexto, getLetraCor
 * que estava espalhado em 20+ lugares.
 * 
 * GRASP - Pure Fabrication: Utilitário de apresentação
 * 
 * @example
 * ```tsx
 * // Antes (prop drilling):
 * <Component getCoresBg={getCoresBg} getCorTexto={getCorTexto} getLetraCor={getLetraCor} />
 * 
 * // Depois:
 * const { getCoresBg, getCorTexto, getLetraCor } = useCardColors()
 * ```
 */

import { useCallback } from 'react'
import { 
  getCoresBgClass, 
  getCorTextoClass, 
  getLetraCor as getLetraCorUtil 
} from '@/lib/gameRules'

// ============================================
// TIPOS
// ============================================

export interface UseCardColorsReturn {
  /** Retorna classe CSS de background para a cor da carta */
  getCoresBg: (cor: string) => string
  /** Retorna classe CSS de texto para a cor da carta */
  getCorTexto: (cor: string) => string
  /** Retorna letra representativa da cor */
  getLetraCor: (cor: string) => string
}

// ============================================
// HOOK PRINCIPAL
// ============================================

/**
 * Hook que fornece funções de cores de cartas
 * 
 * Benefícios:
 * - Elimina prop drilling em múltiplas camadas
 * - Centraliza lógica de cores
 * - Facilita testes (pode ser mockado)
 * 
 * @returns Objeto com funções de cores
 */
export function useCardColors(): UseCardColorsReturn {
  // Memoiza as funções para evitar re-renders desnecessários
  const getCoresBg = useCallback((cor: string) => getCoresBgClass(cor), [])
  const getCorTexto = useCallback((cor: string) => getCorTextoClass(cor), [])
  const getLetraCor = useCallback((cor: string) => getLetraCorUtil(cor), [])
  
  return {
    getCoresBg,
    getCorTexto,
    getLetraCor
  }
}

// ============================================
// EXPORTS DIRETOS PARA USO ESTÁTICO
// ============================================

/**
 * Re-exports das funções para uso direto (sem hook)
 * Útil quando não precisa de memoização ou em componentes que não são React
 */
export {
  getCoresBgClass as getCoresBg,
  getCorTextoClass as getCorTexto,
  getLetraCorUtil as getLetraCor
}

export default useCardColors
