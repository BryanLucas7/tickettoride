/**
 * CAMADA DE SERVIÇOS - API CLIENT
 * ================================
 * 
 * Camada de indireção entre Frontend e Backend.
 * Centraliza todas as chamadas à API FastAPI.
 * 
 * Princípios GRASP aplicados:
 * - Low Coupling: Frontend não conhece detalhes de implementação do backend
 * - Indirection: Esta camada medeia comunicação entre UI e API
 * - Pure Fabrication: Classe de serviço não representa conceito do domínio
 * - High Cohesion: Focada apenas em comunicação com API
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Classe de erro personalizada para API
 */
export class ApiError extends Error {
    constructor(
        message: string,
        public status: number,
        public data?: any
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

/**
 * Cliente HTTP genérico
 * 
 * GRASP - Pure Fabrication:
 * Classe auxiliar que não representa conceito do domínio
 */
class HttpClient {
    private baseUrl: string;
    
    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }
    
    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;
        
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
    
    async post<T>(endpoint: string, data?: any): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'POST',
            body: data ? JSON.stringify(data) : undefined,
        });
    }
    
    async put<T>(endpoint: string, data?: any): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'PUT',
            body: data ? JSON.stringify(data) : undefined,
        });
    }
    
    async delete<T>(endpoint: string): Promise<T> {
        return this.request<T>(endpoint, { method: 'DELETE' });
    }
}

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
        this.http = new HttpClient(API_BASE_URL);
    }
    
    // ========================================
    // SETUP DO JOGO
    // ========================================
    
    /**
     * Cria novo jogo
     */
    async criarJogo(data: {
        jogadores: { nome: string; cor: string }[];
    }) {
        return this.http.post('/api/jogo', data);
    }
    
    /**
     * Obtém estado atual do jogo
     */
    async obterEstadoJogo(jogoId: string) {
        return this.http.get(`/api/jogo/${jogoId}`);
    }
    
    // ========================================
    // AÇÕES DE TURNO
    // ========================================
    
    /**
     * Compra cartas de vagão
     */
    async comprarCartas(jogoId: string, data: {
        jogador_id: string;
        cartas_compradas?: string[]; // IDs das cartas da mesa (se escolhidas)
    }) {
        return this.http.post(`/api/jogo/${jogoId}/comprar-cartas`, data);
    }
    
    /**
     * Conquista rota
     */
    async conquistarRota(jogoId: string, data: {
        jogador_id: string;
        rota_id: string;
        cartas_usadas: string[]; // IDs das cartas da mão
    }) {
        return this.http.post(`/api/jogo/${jogoId}/conquistar-rota`, data);
    }
    
    /**
     * Compra bilhetes de destino
     */
    async comprarBilhetes(jogoId: string, data: {
        jogador_id: string;
        bilhetes_escolhidos: string[]; // IDs dos bilhetes sorteados que o jogador quer manter
        bilhetes_descartados: string[]; // IDs dos bilhetes que não quer
    }) {
        return this.http.post(`/api/jogo/${jogoId}/comprar-bilhetes`, data);
    }
    
    /**
     * Sorteia bilhetes para escolha
     */
    async sortearBilhetes(jogoId: string, data: {
        jogador_id: string;
        quantidade?: number; // Padrão: 3
    }) {
        return this.http.post(`/api/jogo/${jogoId}/sortear-bilhetes`, data);
    }
    
    /**
     * Finaliza turno do jogador
     */
    async finalizarTurno(jogoId: string, data: {
        jogador_id: string;
    }) {
        return this.http.post(`/api/jogo/${jogoId}/finalizar-turno`, data);
    }
    
    // ========================================
    // CONSULTAS
    // ========================================
    
    /**
     * Obtém mão de cartas do jogador
     */
    async obterMaoJogador(jogoId: string, jogadorId: string) {
        return this.http.get(`/api/jogo/${jogoId}/jogador/${jogadorId}/mao`);
    }
    
    /**
     * Obtém bilhetes de destino do jogador
     */
    async obterBilhetesJogador(jogoId: string, jogadorId: string) {
        return this.http.get(`/api/jogo/${jogoId}/jogador/${jogadorId}/bilhetes`);
    }
    
    /**
     * Obtém placar atual
     */
    async obterPlacar(jogoId: string) {
        return this.http.get(`/api/jogo/${jogoId}/placar`);
    }
    
    /**
     * Obtém rotas disponíveis no mapa
     */
    async obterRotas(jogoId: string) {
        return this.http.get(`/api/jogo/${jogoId}/rotas`);
    }
    
    /**
     * Obtém cartas viradas na mesa
     */
    async obterCartasMesa(jogoId: string) {
        return this.http.get(`/api/jogo/${jogoId}/cartas-mesa`);
    }
    
    // ========================================
    // FIM DE JOGO
    // ========================================
    
    /**
     * Verifica se jogo acabou
     */
    async verificarFimJogo(jogoId: string) {
        return this.http.get(`/api/jogo/${jogoId}/fim-jogo`);
    }
    
    /**
     * Obtém pontuação final de todos os jogadores
     */
    async obterPontuacaoFinal(jogoId: string) {
        return this.http.get(`/api/jogo/${jogoId}/pontuacao-final`);
    }
    
    // ========================================
    // VALIDAÇÕES
    // ========================================
    
    /**
     * Valida se jogador pode conquistar rota
     */
    async validarConquistaRota(jogoId: string, data: {
        jogador_id: string;
        rota_id: string;
        cartas_usadas: string[];
    }) {
        return this.http.post(`/api/jogo/${jogoId}/validar-rota`, data);
    }
}

/**
 * Instância singleton do cliente de API
 * 
 * GRASP - Singleton Pattern (implícito):
 * Apenas uma instância do cliente é necessária
 */
export const gameApi = new GameApiClient();

/**
 * Hook personalizado para usar API com estados de loading/erro
 * 
 * Facilita uso nos componentes React
 */
export function useApiCall<T>() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [data, setData] = useState<T | null>(null);
    
    const execute = async (apiCall: () => Promise<T>) => {
        setLoading(true);
        setError(null);
        
        try {
            const result = await apiCall();
            setData(result);
            return result;
        } catch (err) {
            const errorMessage = err instanceof ApiError 
                ? err.message 
                : 'Erro desconhecido';
            setError(errorMessage);
            throw err;
        } finally {
            setLoading(false);
        }
    };
    
    return { execute, loading, error, data };
}

// Exporta apenas para uso em componentes React
import { useState } from 'react';
