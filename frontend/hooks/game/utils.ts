/**
 * Utilitários compartilhados entre hooks de jogo
 * 
 * GRASP - Pure Fabrication: Funções auxiliares que não pertencem
 * a nenhuma entidade específica do domínio.
 */

import { ApiError } from "@/lib/services/gameApi"
import { type ApiErrorResponse, extractApiErrorMessage } from "@/types/api"

/**
 * Handler padronizado para erros da API
 * 
 * Padrão DRY: Centraliza o tratamento de erros que se repetia em
 * useCardPurchase, useRouteConquest e useTicketFlow.
 * 
 * @param error - Erro capturado no catch
 * @param setMensagem - Função para definir mensagem de feedback
 * @param acaoFallback - Mensagem de fallback para erro genérico
 * 
 * @example
 * ```typescript
 * try {
 *   await gameApi.conquerRoute(...)
 * } catch (error) {
 *   handleApiError(error, setMensagem, "Erro ao conquistar rota")
 * }
 * ```
 */
export function handleApiError(
  error: unknown,
  setMensagem: (msg: string) => void,
  acaoFallback: string
): void {
  const mensagem = extractErrorMessage(error, acaoFallback)
  setMensagem(`❌ ${mensagem}`)
}

/**
 * Extrai mensagem de erro de forma consistente
 * 
 * Útil quando você precisa da mensagem para dispatch em reducer
 * além de mostrar ao usuário.
 * 
 * @param error - Erro capturado no catch
 * @param fallback - Mensagem de fallback para erro genérico
 * @returns Mensagem de erro extraída
 * 
 * @example
 * ```typescript
 * catch (error) {
 *   const mensagem = extractErrorMessage(error, "Erro ao comprar carta")
 *   setMensagem(`❌ ${mensagem}`)
 *   dispatch({ type: 'ERRO', mensagem })
 * }
 * ```
 */
export function extractErrorMessage(error: unknown, fallback: string): string {
  if (error instanceof ApiError) {
    const errorResponse = error.data as ApiErrorResponse | undefined
    return extractApiErrorMessage(errorResponse) || error.message || fallback
  }
  return fallback
}

/**
 * Função utilitária para lidar com conclusão de turno
 * 
 * Padrão repetido em múltiplos hooks (useCardPurchase, useRouteConquest, useTicketFlow):
 * 1. Busca estado do jogo
 * 2. Após delay, mostra mensagem de turno completo
 * 3. Após outro delay, busca estado novamente
 * 
 * @param buscarEstadoJogo - Função para buscar estado do jogo
 * @param setMensagem - Função para definir mensagem de feedback
 * @param gameId - ID do jogo
 * @param nextPlayer - Identificador do próximo jogador (opcional)
 * @param delayMs - Delay antes de mostrar mensagem (padrão: 1500ms)
 */
export async function handleTurnComplete(
  buscarEstadoJogo: (gameId: string) => Promise<void>,
  setMensagem: (msg: string) => void,
  gameId: string,
  nextPlayer?: string | number,
  delayMs: number = 1500
): Promise<void> {
  await buscarEstadoJogo(gameId)
  
  setTimeout(() => {
    setTimeout(async () => {
      await buscarEstadoJogo(gameId)
    }, 2000)
  }, delayMs)
}

/**
 * Constante para chave de armazenamento do gameId
 * Re-exportada de types para conveniência
 */
export { GAME_STORAGE_KEY } from "@/types/game"
