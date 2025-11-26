/**
 * useTicketSelection - Hook para gerenciar seleção de bilhetes
 * 
 * Extrai a lógica de seleção de bilhetes para um hook reutilizável,
 * seguindo o princípio GRASP de Information Expert.
 */

import { useState, useCallback, useMemo } from 'react'

interface UseTicketSelectionOptions {
  /** Número máximo de bilhetes selecionáveis (padrão: 3) */
  maxSelection?: number
  /** Número mínimo de bilhetes que devem ser selecionados (padrão: 2) */
  minSelection?: number
}

interface UseTicketSelectionReturn {
  /** IDs dos bilhetes atualmente selecionados */
  bilhetesSelecionados: string[]
  /** Alterna a seleção de um bilhete */
  toggleBilhete: (bilheteId: string) => void
  /** Verifica se a seleção é válida (entre min e max) */
  isValidSelection: boolean
  /** Verifica se pode selecionar mais bilhetes */
  podeSelecionar: boolean
  /** Limpa todas as seleções */
  reset: () => void
  /** Verifica se um bilhete específico está selecionado */
  isSelected: (bilheteId: string) => boolean
  /** Número de bilhetes selecionados */
  quantidadeSelecionada: number
}

/**
 * Hook para gerenciar seleção de bilhetes de destino
 * 
 * @param options Opções de configuração
 * @returns Objeto com estado e funções para gerenciar seleção
 * 
 * @example
 * const {
 *   bilhetesSelecionados,
 *   toggleBilhete,
 *   isValidSelection,
 *   reset
 * } = useTicketSelection({ maxSelection: 3, minSelection: 2 })
 */
export function useTicketSelection(
  options: UseTicketSelectionOptions = {}
): UseTicketSelectionReturn {
  const { maxSelection = 3, minSelection = 2 } = options
  
  const [bilhetesSelecionados, setBilhetesSelecionados] = useState<string[]>([])
  
  const toggleBilhete = useCallback((bilheteId: string) => {
    setBilhetesSelecionados(prev => {
      if (prev.includes(bilheteId)) {
        // Remove se já está selecionado
        return prev.filter(id => id !== bilheteId)
      }
      // Adiciona se ainda não atingiu o máximo
      if (prev.length < maxSelection) {
        return [...prev, bilheteId]
      }
      return prev
    })
  }, [maxSelection])
  
  const reset = useCallback(() => {
    setBilhetesSelecionados([])
  }, [])
  
  const isSelected = useCallback((bilheteId: string) => {
    return bilhetesSelecionados.includes(bilheteId)
  }, [bilhetesSelecionados])
  
  const isValidSelection = useMemo(() => {
    return bilhetesSelecionados.length >= minSelection && 
           bilhetesSelecionados.length <= maxSelection
  }, [bilhetesSelecionados.length, minSelection, maxSelection])
  
  const podeSelecionar = useMemo(() => {
    return bilhetesSelecionados.length < maxSelection
  }, [bilhetesSelecionados.length, maxSelection])
  
  return {
    bilhetesSelecionados,
    toggleBilhete,
    isValidSelection,
    podeSelecionar,
    reset,
    isSelected,
    quantidadeSelecionada: bilhetesSelecionados.length
  }
}

export default useTicketSelection
