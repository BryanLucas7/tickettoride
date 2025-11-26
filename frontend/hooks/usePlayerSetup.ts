/**
 * usePlayerSetup - Hook para gerenciamento de jogadores no setup
 * 
 * Extrai a lógica de criação e validação de jogadores para um hook reutilizável,
 * seguindo os princípios GRASP de Information Expert e High Cohesion.
 */

import { useState, useCallback, useMemo } from 'react'
import type { CorJogador } from '@/types/game'

// Re-export para backward compatibility
export type { CorJogador } from '@/types/game'

/** Cores disponíveis para jogadores (lowercase para compatibilidade com backend) */
export const CORES_DISPONIVEIS: readonly CorJogador[] = ['vermelho', 'azul', 'verde', 'amarelo', 'roxo'] as const

export interface JogadorSetup {
  nome: string
  cor: CorJogador
}

interface UsePlayerSetupOptions {
  /** Número máximo de jogadores permitido (padrão: 5) */
  maxJogadores?: number
  /** Número mínimo de jogadores permitido (padrão: 2) */
  minJogadores?: number
  /** Jogadores iniciais (padrão: 1 jogador vazio) */
  jogadoresIniciais?: JogadorSetup[]
}

interface ValidacaoSetup {
  /** Se todos os nomes estão preenchidos */
  todosPreenchidos: boolean
  /** Se não há cores duplicadas */
  semCoresDuplicadas: boolean
  /** Se a quantidade de jogadores é válida */
  quantidadeValida: boolean
  /** Cores que estão duplicadas (se houver) */
  coresDuplicadas: CorJogador[]
}

interface UsePlayerSetupReturn {
  /** Lista de jogadores */
  jogadores: JogadorSetup[]
  /** Adiciona um novo jogador com cor disponível */
  adicionarJogador: () => void
  /** Remove jogador no índice especificado */
  removerJogador: (index: number) => void
  /** Atualiza campo específico de um jogador */
  atualizarJogador: (index: number, campo: keyof JogadorSetup, valor: string) => void
  /** Objeto de validação */
  validacao: ValidacaoSetup
  /** Se o setup está válido para iniciar o jogo */
  isValid: boolean
  /** Se pode adicionar mais jogadores */
  podeAdicionar: boolean
  /** Se pode remover jogadores */
  podeRemover: boolean
  /** Verifica se uma cor já está em uso por outro jogador */
  corEmUso: (cor: CorJogador, excludeIndex?: number) => boolean
  /** Reseta para estado inicial */
  reset: () => void
}

/**
 * Hook para gerenciar configuração de jogadores
 * 
 * @param options Opções de configuração
 * @returns Objeto com estado e funções para gerenciar jogadores
 * 
 * @example
 * const {
 *   jogadores,
 *   adicionarJogador,
 *   removerJogador,
 *   atualizarJogador,
 *   isValid
 * } = usePlayerSetup({ maxJogadores: 5, minJogadores: 2 })
 */
export function usePlayerSetup(
  options: UsePlayerSetupOptions = {}
): UsePlayerSetupReturn {
  const {
    maxJogadores = 5,
    minJogadores = 2,
    jogadoresIniciais = [{ nome: "", cor: 'vermelho' as CorJogador }]
  } = options
  
  const [jogadores, setJogadores] = useState<JogadorSetup[]>(jogadoresIniciais)
  
  /**
   * Encontra a próxima cor disponível que não está em uso
   */
  const proximaCorDisponivel = useCallback((): CorJogador => {
    const coresEmUso = new Set(jogadores.map(j => j.cor))
    return CORES_DISPONIVEIS.find(cor => !coresEmUso.has(cor)) || CORES_DISPONIVEIS[0]
  }, [jogadores])
  
  /**
   * Verifica se uma cor está em uso por outro jogador
   */
  const corEmUso = useCallback((cor: CorJogador, excludeIndex?: number): boolean => {
    return jogadores.some((j, i) => i !== excludeIndex && j.cor === cor)
  }, [jogadores])
  
  /**
   * Adiciona um novo jogador se não exceder o limite
   */
  const adicionarJogador = useCallback(() => {
    if (jogadores.length < maxJogadores) {
      const novaCor = proximaCorDisponivel()
      setJogadores(prev => [...prev, { nome: "", cor: novaCor }])
    }
  }, [jogadores.length, maxJogadores, proximaCorDisponivel])
  
  /**
   * Remove jogador no índice especificado se não ficar abaixo do mínimo
   */
  const removerJogador = useCallback((index: number) => {
    if (jogadores.length > minJogadores) {
      setJogadores(prev => prev.filter((_, i) => i !== index))
    }
  }, [jogadores.length, minJogadores])
  
  /**
   * Atualiza um campo específico de um jogador
   */
  const atualizarJogador = useCallback((
    index: number,
    campo: keyof JogadorSetup,
    valor: string
  ) => {
    setJogadores(prev => {
      const novos = [...prev]
      novos[index] = { ...novos[index], [campo]: valor }
      return novos
    })
  }, [])
  
  /**
   * Reseta para o estado inicial
   */
  const reset = useCallback(() => {
    setJogadores(jogadoresIniciais)
  }, [jogadoresIniciais])
  
  /**
   * Validação do estado atual
   */
  const validacao = useMemo((): ValidacaoSetup => {
    const todosPreenchidos = jogadores.every(j => j.nome.trim() !== "")
    
    const coresUsadas = jogadores.map(j => j.cor)
    const coresDuplicadas = coresUsadas.filter(
      (cor, index) => coresUsadas.indexOf(cor) !== index
    ) as CorJogador[]
    const semCoresDuplicadas = coresDuplicadas.length === 0
    
    const quantidadeValida = jogadores.length >= minJogadores && jogadores.length <= maxJogadores
    
    return {
      todosPreenchidos,
      semCoresDuplicadas,
      quantidadeValida,
      coresDuplicadas: [...new Set(coresDuplicadas)] // Remove duplicatas na lista de duplicadas
    }
  }, [jogadores, minJogadores, maxJogadores])
  
  const isValid = useMemo(() => {
    return validacao.todosPreenchidos && 
           validacao.semCoresDuplicadas && 
           validacao.quantidadeValida
  }, [validacao])
  
  const podeAdicionar = jogadores.length < maxJogadores
  const podeRemover = jogadores.length > minJogadores
  
  return {
    jogadores,
    adicionarJogador,
    removerJogador,
    atualizarJogador,
    validacao,
    isValid,
    podeAdicionar,
    podeRemover,
    corEmUso,
    reset
  }
}

export default usePlayerSetup
