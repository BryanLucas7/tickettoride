/**
 * useToggleSelection - Hook para gerenciar seleção múltipla com toggle
 * 
 * REFATORAÇÃO DRY: Extrai lógica de toggle selection que estava
 * duplicada em useRouteConquest.ts e useTicketFlow.ts
 * 
 * GRASP - Pure Fabrication: Utilitário de seleção reutilizável
 * GRASP - Low Coupling: Sem dependências de domínio específico
 * 
 * @example
 * ```typescript
 * // Para seleção de cartas (com limite máximo)
 * const { selected, toggle, reset } = useToggleSelection<number>({ max: rotaComprimento })
 * 
 * // Para seleção de bilhetes (com limite mínimo)
 * const { selected, toggle, reset } = useToggleSelection<number>({ min: 1 })
 * 
 * // Para seleção com ambos limites
 * const { selected, toggle } = useToggleSelection<string>({ min: 2, max: 3 })
 * ```
 */

import { useState, useCallback, useMemo } from 'react'

// ============================================
// TIPOS
// ============================================

export interface UseToggleSelectionOptions {
  /** Mínimo de itens que devem permanecer selecionados (não permite deselect abaixo disso) */
  min?: number
  /** Máximo de itens que podem ser selecionados (bloqueia novas seleções acima disso) */
  max?: number
  /** Valores iniciais selecionados */
  initialValues?: number[]
}

export interface UseToggleSelectionReturn<T> {
  /** Array de itens atualmente selecionados */
  selected: T[]
  /** Alterna a seleção de um item */
  toggle: (item: T, overrideMax?: number) => void
  /** Limpa todas as seleções */
  reset: () => void
  /** Substitui todas as seleções */
  setSelected: React.Dispatch<React.SetStateAction<T[]>>
  /** Verifica se um item está selecionado */
  isSelected: (item: T) => boolean
  /** Número de itens selecionados */
  count: number
  /** Se atingiu o limite máximo */
  isAtMax: boolean
  /** Se está no limite mínimo (não pode deselecionar) */
  isAtMin: boolean
  /** Se a seleção é válida (entre min e max) */
  isValid: boolean
}

// ============================================
// HOOK PRINCIPAL
// ============================================

/**
 * Hook genérico para gerenciar seleção múltipla com toggle
 * 
 * @param options Configurações de limite mínimo/máximo
 * @returns Objeto com estado e funções de controle
 */
export function useToggleSelection<T = number>(
  options: UseToggleSelectionOptions = {}
): UseToggleSelectionReturn<T> {
  const { min = 0, max, initialValues = [] } = options
  
  const [selected, setSelected] = useState<T[]>(initialValues as unknown as T[])
  
  /**
   * Alterna a seleção de um item
   * @param item Item a ser toggled
   * @param overrideMax Limite máximo temporário (útil para cartas onde o limite depende da rota)
   */
  const toggle = useCallback((item: T, overrideMax?: number) => {
    setSelected((current) => {
      const isCurrentlySelected = current.includes(item)
      
      if (isCurrentlySelected) {
        // Tentando deselecionar
        if (current.length <= min) {
          // Não permite deselecionar abaixo do mínimo
          return current
        }
        return current.filter((i) => i !== item)
      } else {
        // Tentando selecionar
        const effectiveMax = overrideMax ?? max
        if (typeof effectiveMax === 'number' && current.length >= effectiveMax) {
          // Não permite selecionar acima do máximo
          return current
        }
        return [...current, item]
      }
    })
  }, [min, max])
  
  /**
   * Limpa todas as seleções
   */
  const reset = useCallback(() => {
    setSelected([])
  }, [])
  
  /**
   * Verifica se um item está selecionado
   */
  const isSelected = useCallback((item: T) => {
    return selected.includes(item)
  }, [selected])
  
  /**
   * Valores derivados computados
   */
  const derivedState = useMemo(() => {
    const count = selected.length
    const isAtMax = typeof max === 'number' && count >= max
    const isAtMin = count <= min
    const isValid = count >= min && (typeof max !== 'number' || count <= max)
    
    return { count, isAtMax, isAtMin, isValid }
  }, [selected.length, min, max])
  
  return {
    selected,
    toggle,
    reset,
    setSelected,
    isSelected,
    ...derivedState
  }
}

export default useToggleSelection
