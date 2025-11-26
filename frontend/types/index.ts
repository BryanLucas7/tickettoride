/**
 * Módulo de Tipos - Exportações Centralizadas
 * 
 * Este arquivo re-exporta todos os tipos públicos do projeto.
 * Importe tipos deste módulo para ter acesso centralizado.
 * 
 * @example
 * import { Jogador, StatusTurno, ApiErrorResponse } from '@/types'
 * import { JogadorId, asJogadorId } from '@/types'
 * import { DrawCardResponse, ConquerRouteResponse } from '@/types'
 * 
 * ESTRUTURA DE ARQUIVOS:
 * - branded.ts: Branded types para IDs (JogadorId, GameId, etc.)
 * - game.ts: Entidades do domínio (Jogador, Rota, Carta, etc.)
 * - api.ts: Tipos de request/response da API
 * - ui.ts: Tipos específicos de UI/componentes
 * 
 * CONVENÇÕES:
 * - `interface` para objetos e props de componentes
 * - `type` para unions, aliases e tipos utilitários
 * - `enum` para conjuntos fixos de valores
 * - `Branded Types` para IDs únicos (JogadorId, GameId, etc.)
 * 
 * Veja CONVENTIONS.md para documentação completa.
 */

// ============================================
// BRANDED TYPES (IDs SEGUROS)
// ============================================

export {
  // Tipos de ID
  type JogadorId,
  type GameId,
  type RotaId,
  type BilheteId,
  
  // Funções de Conversão de ID
  asJogadorId,
  asGameId,
  asRotaId,
  asBilheteId,
  
  // Funções de Validação
  isValidId,
  toJogadorId,
  toGameId,
  toRotaId,
  toBilheteId,
} from './branded'

// ============================================
// TIPOS DO DOMÍNIO DO JOGO
// ============================================

export {
  // Enums
  CorCarta,
  
  // Union Types (Literal Types para cores)
  type StatusTurno,
  type StatusJogo,
  type CorJogador,
  type CorRotaString,
  type CorCartaString,
  type CorMapa,
  
  // Interfaces de Entidades
  type Jogador,
  type CartaVagao,
  type CartaVagaoUI,
  type Rota,
  type BilheteDestino,
  type BilheteDestinoUI,
  type MaiorCaminhoLeader,
  type MaiorCaminhoStatus,
  type GameState,
  
  // Funções de Conversão e Helpers
  toCorCarta,
  toCartaVagaoUI,
  toBilheteDestinoUI,
  isCorMapa,
  obterCorMapa,
  
  // Constantes
  PONTOS_ROTA,
  MAPA_CORES_FINAIS,
  DEFAULT_API_URL,
  GAME_STORAGE_KEY,
} from './game'

// ============================================
// TIPOS DE API - RESPOSTAS E ERROS
// ============================================

export {
  // Tipos Genéricos de Resposta
  type ApiSuccessResponse,
  type ApiFailureResponse,
  type ApiResponse,
  isApiSuccess,
  isApiFailure,
  
  // Interfaces de Erro
  type ApiErrorDetail,
  type ApiErrorResponse,
  isApiErrorDetailArray,
  extractApiErrorMessage,
  
  // Respostas de Cartas
  type DrawCardResponse,
  type PlayerCardsResponse,
  
  // Respostas de Bilhetes
  type BuyTicketsResponse,
  type TicketsPreviewResponse,
  type PlayerTicketsResponse,
  
  // Respostas de Rotas
  type ConquerRouteResponse,
  type RoutesResponse,
  
  // Respostas de Mapa
  type CidadeMapaApi,
  type RotaMapaApi,
  type MapConfigResponse,
  
  // Interfaces de Pontuação
  type BilhetePontuacaoApi,
  type PontuacaoApi,
  type PontuacaoFinalApiResponse,
  
  // Interfaces de Storage
  type JogadorStorage,
  type JogadorComBilhetes,
} from './api'

// ============================================
// TIPOS DE UI - COMPONENTES REACT
// ============================================

export {
  // Tipos de Cores
  type CorSistema,
  type ColorGetter,
  type ColorHelpers,
  
  // Props de Componentes
  type JogadorDisplayProps,
  type ContadorProps,
  
  // Estados de UI
  type LoadingState,
  type ModalState,
  type NotificationState,
  
  // Configuração Visual
  type PlayerColorConfig,
  type Position,
  type Dimensions,
  
  // Callbacks de Eventos
  type SelectionCallback,
  type ActionCallback,
  type AsyncActionCallback,
  
  // Formulários
  type FormFieldState,
  type FormValidationResult,
} from './ui'
