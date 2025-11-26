/**
 * useGameSetup - Hook para configuração e criação de jogos
 * 
 * Princípios GRASP aplicados:
 * - SRP: Responsabilidade única de gerenciar criação de jogos
 * - Low Coupling: Isolado da UI, apenas lógica de negócio
 * - Information Expert: Concentra conhecimento sobre criação de jogos
 * 
 * Extraído de setup/page.tsx seguindo princípio de separação de concerns
 * 
 * DRY REFACTORING: 
 * - Usa storageService centralizado para localStorage
 * - Usa gameApi centralizado para chamadas HTTP
 */

import { useCallback, useState } from 'react'
import { gameApi, ApiError } from '@/lib/services/gameApi'
import { storageService } from '@/lib/services/storageService'
import type { CorJogador, JogadorId } from '@/types/game'

// ============================================
// TIPOS
// ============================================

export interface JogadorSetup {
  nome: string
  cor: CorJogador
}

export interface GameCreationResult {
  gameId: string
  jogadores: Array<{
    id: JogadorId
    nome: string
    cor: CorJogador
  }>
}

export interface UseGameSetupReturn {
  /** Cria um novo jogo no backend */
  criarJogo: (jogadores: JogadorSetup[]) => Promise<GameCreationResult>
  /** Indica se está criando o jogo */
  criandoJogo: boolean
  /** Mensagem de erro, se houver */
  erro: string | null
  /** Limpa dados do jogo anterior do localStorage */
  limparDadosAnteriores: () => void
  /** Salva dados do jogo no localStorage */
  salvarDadosJogo: (gameId: string, jogadores: GameCreationResult['jogadores']) => void
}

// ============================================
// HOOK PRINCIPAL
// ============================================

/**
 * Hook para gerenciar criação de jogos
 * 
 * @example
 * ```tsx
 * const { criarJogo, criandoJogo, erro } = useGameSetup()
 * 
 * const handleIniciar = async () => {
 *   try {
 *     const result = await criarJogo(jogadores)
 *     router.push('/bilhetes-destino')
 *   } catch (error) {
 *     // erro já está disponível no estado
 *   }
 * }
 * ```
 */
export function useGameSetup(): UseGameSetupReturn {
  const [criandoJogo, setCriandoJogo] = useState(false)
  const [erro, setErro] = useState<string | null>(null)

  const limparDadosAnteriores = useCallback(() => {
    storageService.clearGameData()
  }, [])

  const salvarDadosJogo = useCallback(
    (gameId: string, jogadores: GameCreationResult['jogadores']) => {
      storageService.setGameData(gameId, jogadores)
    },
    []
  )

  const criarJogo = useCallback(
    async (jogadores: JogadorSetup[]): Promise<GameCreationResult> => {
      setCriandoJogo(true)
      setErro(null)

      try {
        // Limpar dados antigos antes de criar novo jogo
        storageService.clearGameData()

        console.log('🎮 Criando novo jogo...')

        const gameData = await gameApi.createGame({
          numero_jogadores: jogadores.length,
          jogadores: jogadores.map((j) => ({
            nome: j.nome,
            cor: j.cor
          }))
        })

        console.log('✅ Jogo criado com sucesso:', gameData)

        // Salvar dados automaticamente
        storageService.setGameData(gameData.game_id, gameData.jogadores)

        return {
          gameId: gameData.game_id,
          jogadores: gameData.jogadores as GameCreationResult['jogadores']
        }
      } catch (error) {
        let mensagemCompleta: string
        
        if (error instanceof ApiError) {
          mensagemCompleta = `Erro ao criar jogo: ${error.message}`
          if (error.status === 0) {
            mensagemCompleta += '\n\nCertifique-se de que o backend Python está rodando na porta 8000'
          }
        } else {
          const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido'
          mensagemCompleta = `Erro ao criar jogo: ${errorMessage}\n\nCertifique-se de que o backend Python está rodando na porta 8000`
        }
        
        console.error('❌ Erro ao criar jogo:', error)
        setErro(mensagemCompleta)
        throw new Error(mensagemCompleta)
      } finally {
        setCriandoJogo(false)
      }
    },
    []
  )

  return {
    criarJogo,
    criandoJogo,
    erro,
    limparDadosAnteriores,
    salvarDadosJogo
  }
}
