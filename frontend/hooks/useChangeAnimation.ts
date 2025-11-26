/**
 * useChangeAnimation - Hook genérico para detectar e animar mudanças em arrays
 * 
 * Este hook detecta quando valores em um array de items mudam e mantém
 * um registro das mudanças para animação.
 * 
 * Princípio GRASP - Low Coupling:
 * Hook genérico que pode ser usado por qualquer componente que precise
 * animar mudanças em valores numéricos.
 * 
 * @example
 * // Uso em TrilhaPontuacao
 * const mudancas = useChangeAnimation(
 *   jogadores,
 *   (jogador) => jogador.pontos,
 *   { animationDuration: 2000, enabled: animarMudancas }
 * )
 * 
 * // Uso em ContadorTrens
 * const mudancas = useChangeAnimation(
 *   jogadores,
 *   (jogador) => jogador.trensRestantes,
 *   { animationDuration: 2000, enabled: animarMudancas }
 * )
 */

import { useState, useEffect, useRef, useCallback } from 'react'

interface UseChangeAnimationOptions {
  /** Duração da animação em milissegundos (padrão: 2000) */
  animationDuration?: number
  /** Se a animação está habilitada (padrão: true) */
  enabled?: boolean
}

/**
 * Hook para detectar e animar mudanças em valores de items
 * 
 * @param items Array de items com propriedade 'id'
 * @param getValue Função para extrair o valor numérico de cada item
 * @param options Opções de configuração
 * @returns Record com as mudanças detectadas (id -> diferença)
 */
export function useChangeAnimation<T extends { id: string }>(
  items: T[],
  getValue: (item: T) => number,
  options: UseChangeAnimationOptions = {}
): Record<string, number> {
  const { animationDuration = 2000, enabled = true } = options
  
  // Usa useRef para armazenar estado anterior sem causar re-renders
  const previousItemsRef = useRef<T[]>(items)
  const [mudancas, setMudancas] = useState<Record<string, number>>({})
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  
  // Memoiza getValue para evitar re-execuções desnecessárias
  const getValueStable = useCallback(getValue, [])
  
  useEffect(() => {
    if (!enabled) return
    
    const novasMudancas: Record<string, number> = {}
    
    items.forEach(item => {
      const anterior = previousItemsRef.current.find(i => i.id === item.id)
      if (anterior) {
        const valorAtual = getValueStable(item)
        const valorAnterior = getValueStable(anterior)
        const diff = valorAtual - valorAnterior
        if (diff !== 0) {
          novasMudancas[item.id] = diff
        }
      }
    })
    
    if (Object.keys(novasMudancas).length > 0) {
      setMudancas(novasMudancas)
      
      // Limpa timeout anterior se existir
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
      
      // Remove indicadores de mudança após o tempo de animação
      timeoutRef.current = setTimeout(() => {
        setMudancas({})
      }, animationDuration)
    }
    
    // Atualiza referência para comparação futura
    previousItemsRef.current = items
  }, [items, enabled, animationDuration, getValueStable])
  
  // Cleanup do timeout quando componente desmonta
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])
  
  return mudancas
}

/**
 * Hook auxiliar para detectar alerta de fim de jogo baseado em threshold
 * 
 * @param items Array de items
 * @param getValue Função para extrair o valor numérico
 * @param threshold Valor limite para ativar o alerta
 * @returns boolean indicando se algum item está abaixo do threshold
 */
export function useThresholdAlert<T>(
  items: T[],
  getValue: (item: T) => number,
  threshold: number
): boolean {
  const [alerta, setAlerta] = useState(false)
  
  useEffect(() => {
    const temAlerta = items.some(item => getValue(item) <= threshold)
    setAlerta(temAlerta)
  }, [items, getValue, threshold])
  
  return alerta
}

export default useChangeAnimation
