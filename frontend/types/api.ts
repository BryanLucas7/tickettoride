/**
 * Tipos de API - Respostas e Erros do Backend
 * 
 * Este arquivo centraliza todos os tipos relacionados à comunicação
 * com a API do backend, incluindo respostas e tratamento de erros.
 * 
 * @module types/api
 */

import type { CartaVagao, Rota, BilheteDestino, CorJogador } from './game'
import type { JogadorId } from './branded'

// ============================================
// TIPOS GENÉRICOS DE API
// ============================================

/**
 * Resposta genérica de sucesso da API
 */
export interface ApiSuccessResponse<T = unknown> {
  success: true
  message?: string
  data?: T
}

/**
 * Resposta genérica de erro da API
 */
export interface ApiFailureResponse {
  success: false
  message: string
  error?: string
  details?: unknown
}

/**
 * Resposta genérica da API (discriminated union)
 */
export type ApiResponse<T = unknown> = ApiSuccessResponse<T> | ApiFailureResponse

/**
 * Type guard para verificar se resposta foi sucesso
 */
export function isApiSuccess<T>(response: ApiResponse<T>): response is ApiSuccessResponse<T> {
  return response.success === true
}

/**
 * Type guard para verificar se resposta foi erro
 */
export function isApiFailure(response: ApiResponse<unknown>): response is ApiFailureResponse {
  return response.success === false
}

// ============================================
// TIPOS DE ERRO DE API
// ============================================

/**
 * Detalhe de erro de validação da API (formato FastAPI/Pydantic)
 */
export interface ApiErrorDetail {
  msg?: string
  message?: string
  loc?: (string | number)[]
  type?: string
}

/**
 * Resposta de erro da API
 */
export interface ApiErrorResponse {
  detail?: string | ApiErrorDetail[]
}

/**
 * Type guard para verificar se é um array de detalhes de erro
 */
export function isApiErrorDetailArray(detail: unknown): detail is ApiErrorDetail[] {
  return Array.isArray(detail) && detail.every(
    (item) => typeof item === 'object' && item !== null && ('msg' in item || 'message' in item)
  )
}

/**
 * Extrai mensagem de erro de uma resposta de erro da API
 */
export function extractApiErrorMessage(errorData: unknown): string {
  if (!errorData || typeof errorData !== 'object') {
    return 'Erro desconhecido'
  }

  const response = errorData as ApiErrorResponse

  if (typeof response.detail === 'string') {
    return response.detail
  }

  if (isApiErrorDetailArray(response.detail)) {
    return response.detail.map((d) => d.msg || d.message || '').filter(Boolean).join('; ')
  }

  return 'Erro desconhecido'
}

// ============================================
// TIPOS DE RESPOSTA - CARTAS
// ============================================

/**
 * Resposta ao comprar carta
 */
export interface DrawCardResponse {
  success: boolean
  message: string
  card?: CartaVagao
  turn_completed?: boolean
  next_player?: string
}

/**
 * Resposta com cartas do jogador
 */
export interface PlayerCardsResponse {
  cards: CartaVagao[]
}

// ============================================
// TIPOS DE RESPOSTA - BILHETES
// ============================================

/**
 * Resposta ao comprar bilhetes
 */
export interface BuyTicketsResponse {
  success: boolean
  message: string
  next_player?: string
}

/**
 * Resposta com preview de bilhetes disponíveis
 */
export interface TicketsPreviewResponse {
  tickets: BilheteDestino[]
}

/**
 * Resposta com bilhetes do jogador
 */
export interface PlayerTicketsResponse {
  tickets: BilheteDestino[]
}

// ============================================
// TIPOS DE RESPOSTA - ROTAS
// ============================================

/**
 * Resposta ao conquistar rota
 */
export interface ConquerRouteResponse {
  success: boolean
  message: string
  points?: number
  next_player?: string
}

/**
 * Resposta com rotas do jogo
 */
export interface RoutesResponse {
  routes: Rota[]
}

// ============================================
// TIPOS DE RESPOSTA - MAPA
// ============================================

/**
 * Cidade na configuração do mapa
 */
export interface CidadeMapaApi {
  nome: string
  x: number
  y: number
}

/**
 * Rota na configuração do mapa
 */
export interface RotaMapaApi {
  id: string
  cidadeA: string
  cidadeB: string
  comprimento: number
  cor: string
}

/**
 * Resposta com configuração do mapa
 */
export interface MapConfigResponse {
  cidades: CidadeMapaApi[]
  rotas: RotaMapaApi[]
}

// ============================================
// TIPOS DE PONTUAÇÃO FINAL
// ============================================

/**
 * Bilhete na resposta de pontuação da API
 * Suporta ambos os formatos: (origem/destino) e (cidadeOrigem/cidadeDestino)
 */
export interface BilhetePontuacaoApi {
  origem?: string
  cidadeOrigem?: string
  destino?: string
  cidadeDestino?: string
  pontos?: number
}

/**
 * Pontuação de um jogador na resposta da API
 */
export interface PontuacaoApi {
  jogador_id: JogadorId
  jogador_nome: string
  jogador_cor: CorJogador
  pontos_rotas?: number
  bilhetes_completos?: BilhetePontuacaoApi[]
  bilhetes_incompletos?: BilhetePontuacaoApi[]
  pontos_bilhetes_positivos?: number
  pontos_bilhetes_negativos?: number
  bonus_maior_caminho?: boolean
  pontos_maior_caminho?: number
  pontuacao_total?: number
  tamanho_maior_caminho?: number
}

/**
 * Resposta completa de pontuação final
 */
export interface PontuacaoFinalApiResponse {
  pontuacoes: PontuacaoApi[]
}

// ============================================
// TIPOS DE ARMAZENAMENTO LOCAL
// ============================================

/**
 * Dados do jogador armazenados no localStorage
 */
export interface JogadorStorage {
  id?: string
  nome: string
  cor: string
}

/**
 * Jogador com bilhetes selecionados (usado em bilhetes-destino)
 */
export interface JogadorComBilhetes extends JogadorStorage {
  bilhetesSelecionados: Array<{
    id: string
    cidadeOrigem: string
    cidadeDestino: string
    pontos: number
  }>
}

// ============================================
// TIPOS DE CRIAÇÃO DE JOGO
// ============================================

/**
 * Dados para criar um novo jogo
 */
export interface CreateGameRequest {
  numero_jogadores: number
  jogadores: Array<{
    nome: string
    cor: string
  }>
}

/**
 * Resposta da criação de um novo jogo
 */
export interface CreateGameResponse {
  game_id: string
  jogadores: Array<{
    id: string
    nome: string
    cor: string
  }>
}

/**
 * Resposta de bilhetes iniciais para seleção
 */
export interface InitialTicketsResponse {
  bilhetes: Array<{
    id: string
    cidadeOrigem: string
    cidadeDestino: string
    pontos: number
  }>
}

/**
 * Requisição para confirmar bilhetes iniciais
 */
export interface ConfirmInitialTicketsRequest {
  bilhetes_escolhidos: string[]
}

/**
 * Resposta da confirmação de bilhetes iniciais
 */
export interface ConfirmInitialTicketsResponse {
  success: boolean
  message?: string
}
