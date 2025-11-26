/**
 * CAMADA DE SERVIÇOS - API CLIENT
 * ================================
 * 
 * Camada de indireção entre Frontend e Backend.
 * Centraliza todas as chamadas à API FastAPI.
 * 
 * REFATORAÇÃO DRY: Usa getBackendUrl() de lib/config/api.ts
 * ao invés de duplicar lógica de resolução de URL.
 * 
 * Princípios GRASP aplicados:
 * - Low Coupling: Frontend não conhece detalhes de implementação do backend
 * - Indirection: Esta camada medeia comunicação entre UI e API
 * - Pure Fabrication: Classe de serviço não representa conceito do domínio
 * - High Cohesion: Focada apenas em comunicação com API
 */

import { type GameState } from '@/types/game';
import { getBackendUrl } from '@/lib/config/api';

import {
  type DrawCardResponse,
  type ConquerRouteResponse,
  type BuyTicketsResponse,
  type TicketsPreviewResponse,
  type PlayerCardsResponse,
  type PlayerTicketsResponse,
  type RoutesResponse,
  type MapConfigResponse,
  type PontuacaoFinalApiResponse,
  type PontuacaoApi,
  type CreateGameRequest,
  type CreateGameResponse,
  type InitialTicketsResponse,
  type ConfirmInitialTicketsRequest,
  type ConfirmInitialTicketsResponse,
} from '@/types/api';

// Re-exportar tipos para backward compatibility
export type {
  DrawCardResponse,
  ConquerRouteResponse,
  BuyTicketsResponse,
  TicketsPreviewResponse,
  PlayerCardsResponse,
  PlayerTicketsResponse,
  RoutesResponse,
  MapConfigResponse,
  PontuacaoFinalApiResponse,
  PontuacaoApi,
  CreateGameRequest,
  CreateGameResponse,
  InitialTicketsResponse,
  ConfirmInitialTicketsResponse,
} from '@/types/api';

// ============================================
// CLASSE DE ERRO PERSONALIZADA
// ============================================

/**
 * Classe de erro personalizada para API
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// ============================================
// CLIENTE HTTP GENÉRICO
// ============================================

/**
 * Cliente HTTP genérico
 * 
 * GRASP - Pure Fabrication:
 * Classe auxiliar que não representa conceito do domínio
 * 
 * REFATORAÇÃO DRY: Usa getBackendUrl() centralizado
 */
class HttpClient {
  private getBaseUrl(): string {
    return getBackendUrl();
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.getBaseUrl()}${endpoint}`;

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.detail || 'Erro na requisição',
          response.status,
          errorData
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError('Erro de conexão com o servidor', 0);
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// ============================================
// CLIENTE DE API DO JOGO
// ============================================

/**
 * Cliente de API do Jogo
 * 
 * GRASP - Indirection:
 * Medeia comunicação entre frontend (React) e backend (FastAPI)
 * 
 * GRASP - Low Coupling:
 * Frontend não conhece detalhes de rotas ou estrutura do backend
 */
class GameApiClient {
  private http: HttpClient;

  constructor() {
    this.http = new HttpClient();
  }

  // ========================================
  // CONFIGURAÇÃO DO MAPA
  // ========================================

  /**
   * Obtém configuração do mapa (cidades e rotas)
   */
  async getMapConfig(): Promise<MapConfigResponse> {
    return this.http.get<MapConfigResponse>('/map/config');
  }

  // ========================================
  // ESTADO DO JOGO
  // ========================================

  /**
   * Obtém estado atual do jogo
   */
  async getGameState(gameId: string): Promise<GameState> {
    return this.http.get<GameState>(`/games/${gameId}`);
  }

  /**
   * Obtém rotas do jogo com informações de proprietário
   */
  async getRoutes(gameId: string): Promise<RoutesResponse> {
    return this.http.get<RoutesResponse>(`/games/${gameId}/routes`);
  }

  // ========================================
  // CARTAS DO JOGADOR
  // ========================================

  /**
   * Obtém cartas na mão do jogador
   */
  async getPlayerCards(gameId: string, playerId: string): Promise<PlayerCardsResponse> {
    return this.http.get<PlayerCardsResponse>(`/games/${gameId}/players/${playerId}/cards`);
  }

  /**
   * Compra carta fechada (do baralho)
   */
  async drawClosedCard(gameId: string, playerId: string): Promise<DrawCardResponse> {
    return this.http.post<DrawCardResponse>(`/games/${gameId}/players/${playerId}/draw-closed`);
  }

  /**
   * Compra carta aberta (da mesa)
   */
  async drawOpenCard(gameId: string, playerId: string, cardIndex: number): Promise<DrawCardResponse> {
    return this.http.post<DrawCardResponse>(`/games/${gameId}/players/${playerId}/draw-open/${cardIndex}`);
  }

  // ========================================
  // BILHETES DO JOGADOR
  // ========================================

  /**
   * Obtém bilhetes de destino do jogador
   */
  async getPlayerTickets(gameId: string, playerId: string): Promise<PlayerTicketsResponse> {
    return this.http.get<PlayerTicketsResponse>(`/games/${gameId}/players/${playerId}/tickets`);
  }

  /**
   * Obtém preview de bilhetes disponíveis para compra
   */
  async getTicketsPreview(gameId: string, playerId: string): Promise<TicketsPreviewResponse> {
    return this.http.post<TicketsPreviewResponse>(`/games/${gameId}/players/${playerId}/tickets/preview`);
  }

  /**
   * Compra bilhetes selecionados
   */
  async buyTickets(
    gameId: string,
    playerId: string,
    selectedTicketIndices: string[]
  ): Promise<BuyTicketsResponse> {
    return this.http.post<BuyTicketsResponse>(
      `/games/${gameId}/players/${playerId}/buy-tickets`,
      { bilhetes_escolhidos: selectedTicketIndices }
    );
  }

  // ========================================
  // CONQUISTA DE ROTAS
  // ========================================

  /**
   * Conquista uma rota no mapa
   */
  async conquerRoute(
    gameId: string,
    playerId: string,
    routeId: string,
    cardsUsed: Array<{ cor: string; eh_locomotiva?: boolean }>
  ): Promise<ConquerRouteResponse> {
    return this.http.post<ConquerRouteResponse>(
      `/games/${gameId}/players/${playerId}/conquer-route`,
      {
        rota_id: routeId,
        cartas_usadas: cardsUsed
      }
    );
  }

  // ========================================
  // FIM DE JOGO
  // ========================================

  /**
   * Obtém pontuação final de todos os jogadores
   */
  async getFinalScore(gameId: string): Promise<PontuacaoFinalApiResponse> {
    return this.http.get<PontuacaoFinalApiResponse>(`/games/${gameId}/pontuacao-final`);
  }

  // ========================================
  // CRIAÇÃO DE JOGO
  // ========================================

  /**
   * Cria um novo jogo
   */
  async createGame(request: CreateGameRequest): Promise<CreateGameResponse> {
    return this.http.post<CreateGameResponse>('/games', request);
  }

  // ========================================
  // BILHETES INICIAIS (Setup)
  // ========================================

  /**
   * Obtém bilhetes iniciais para seleção do jogador
   */
  async getInitialTickets(gameId: string, playerId: string): Promise<InitialTicketsResponse> {
    return this.http.get<InitialTicketsResponse>(
      `/games/${gameId}/players/${playerId}/tickets/initial`
    );
  }

  /**
   * Confirma a seleção de bilhetes iniciais
   */
  async confirmInitialTickets(
    gameId: string,
    playerId: string,
    selectedTicketIds: string[]
  ): Promise<ConfirmInitialTicketsResponse> {
    return this.http.post<ConfirmInitialTicketsResponse>(
      `/games/${gameId}/players/${playerId}/tickets/initial`,
      { bilhetes_escolhidos: selectedTicketIds }
    );
  }
}

// ============================================
// INSTÂNCIA SINGLETON
// ============================================

/**
 * Instância singleton do cliente de API
 * 
 * GRASP - Singleton Pattern (implícito):
 * Apenas uma instância do cliente é necessária
 */
export const gameApi = new GameApiClient();
