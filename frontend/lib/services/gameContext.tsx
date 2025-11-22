/**
 * GERENCIADOR DE ESTADO GLOBAL DO JOGO
 * =====================================
 * 
 * Usa React Context para gerenciar estado global do jogo.
 * Sincroniza ações entre componentes e backend.
 * 
 * Princípios GRASP aplicados:
 * - Controller: GameContext coordena ações do jogo
 * - Information Expert: Cada componente conhece suas responsabilidades
 * - Low Coupling: Componentes acessam estado via Context, não diretamente
 * - Indirection: Context medeia acesso ao estado
 */

'use client';

import { createContext, useContext, useState, useCallback, ReactNode, useEffect } from 'react';
import { gameApi } from './gameApi';
import { CartaVagao, CorCarta } from '@/components/MaoCartas';
import { BilheteDestino } from '@/components/PainelBilhetesDestino';
import { JogadorPlacar } from '@/components/TrilhaPontuacao';
import { JogadorTrens } from '@/components/ContadorTrens';

/**
 * Interface do Estado do Jogo
 */
export interface EstadoJogo {
    jogoId: string | null;
    jogadorAtual: string | null; // ID do jogador local
    turnoAtual: string | null;   // ID do jogador cujo turno é agora
    jogadores: JogadorInfo[];
    fase: 'setup' | 'jogando' | 'fim';
    fimJogoAtivado: boolean;
    vencedor: string | null;
}

/**
 * Informações de um Jogador
 */
export interface JogadorInfo {
    id: string;
    nome: string;
    cor: string;
    pontos: number;
    trensRestantes: number;
    quantidadeCartas: number;
    quantidadeBilhetes: number;
}

/**
 * Interface do Context
 */
interface GameContextType {
    // Estado
    estado: EstadoJogo;
    carregando: boolean;
    erro: string | null;
    
    // Ações de Setup
    criarJogo: (jogadores: { nome: string; cor: string }[]) => Promise<void>;
    
    // Ações de Turno
    comprarCartas: (cartasMesa?: string[]) => Promise<void>;
    conquistarRota: (rotaId: string, cartasUsadas: string[]) => Promise<void>;
    comprarBilhetes: (bilhetesEscolhidos: string[], bilhetesDescartados: string[]) => Promise<void>;
    finalizarTurno: () => Promise<void>;
    
    // Consultas
    atualizarEstado: () => Promise<void>;
    obterMao: () => Promise<CartaVagao[]>;
    obterBilhetes: () => Promise<BilheteDestino[]>;
    obterPlacar: () => Promise<JogadorPlacar[]>;
    obterTrens: () => Promise<JogadorTrens[]>;
    
    // Utilitários
    limparErro: () => void;
}

/**
 * Context do Jogo
 * 
 * GRASP - Controller:
 * Coordena todas as ações do jogo entre UI e backend
 */
const GameContext = createContext<GameContextType | undefined>(undefined);

/**
 * Provider do Context
 */
export function GameProvider({ children }: { children: ReactNode }) {
    const [estado, setEstado] = useState<EstadoJogo>({
        jogoId: null,
        jogadorAtual: null,
        turnoAtual: null,
        jogadores: [],
        fase: 'setup',
        fimJogoAtivado: false,
        vencedor: null,
    });
    
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState<string | null>(null);
    
    /**
     * Cria novo jogo
     */
    const criarJogo = useCallback(async (jogadores: { nome: string; cor: string }[]) => {
        setCarregando(true);
        setErro(null);
        
        try {
            const response = await gameApi.criarJogo({ jogadores });
            
            setEstado({
                jogoId: response.jogo_id,
                jogadorAtual: response.jogador_local_id, // Primeiro jogador
                turnoAtual: response.turno_atual,
                jogadores: response.jogadores,
                fase: 'jogando',
                fimJogoAtivado: false,
                vencedor: null,
            });
        } catch (err: any) {
            setErro(err.message);
            throw err;
        } finally {
            setCarregando(false);
        }
    }, []);
    
    /**
     * Atualiza estado completo do jogo
     */
    const atualizarEstado = useCallback(async () => {
        if (!estado.jogoId) return;
        
        setCarregando(true);
        
        try {
            const response = await gameApi.obterEstadoJogo(estado.jogoId);
            
            setEstado(prev => ({
                ...prev,
                turnoAtual: response.turno_atual,
                jogadores: response.jogadores,
                fimJogoAtivado: response.fim_jogo_ativado,
                fase: response.fim_jogo_ativado ? 'fim' : 'jogando',
            }));
            
            // Se jogo acabou, verifica vencedor
            if (response.fim_jogo_ativado) {
                const pontuacaoFinal = await gameApi.obterPontuacaoFinal(estado.jogoId);
                const vencedorInfo = pontuacaoFinal.reduce((max, p) => 
                    p.pontuacaoTotal > max.pontuacaoTotal ? p : max
                );
                
                setEstado(prev => ({
                    ...prev,
                    vencedor: vencedorInfo.jogadorNome,
                }));
            }
        } catch (err: any) {
            setErro(err.message);
        } finally {
            setCarregando(false);
        }
    }, [estado.jogoId]);
    
    /**
     * Compra cartas de vagão
     */
    const comprarCartas = useCallback(async (cartasMesa?: string[]) => {
        if (!estado.jogoId || !estado.jogadorAtual) return;
        
        setCarregando(true);
        setErro(null);
        
        try {
            await gameApi.comprarCartas(estado.jogoId, {
                jogador_id: estado.jogadorAtual,
                cartas_compradas: cartasMesa,
            });
            
            await atualizarEstado();
        } catch (err: any) {
            setErro(err.message);
            throw err;
        } finally {
            setCarregando(false);
        }
    }, [estado.jogoId, estado.jogadorAtual, atualizarEstado]);
    
    /**
     * Conquista rota
     */
    const conquistarRota = useCallback(async (rotaId: string, cartasUsadas: string[]) => {
        if (!estado.jogoId || !estado.jogadorAtual) return;
        
        setCarregando(true);
        setErro(null);
        
        try {
            await gameApi.conquistarRota(estado.jogoId, {
                jogador_id: estado.jogadorAtual,
                rota_id: rotaId,
                cartas_usadas: cartasUsadas,
            });
            
            await atualizarEstado();
        } catch (err: any) {
            setErro(err.message);
            throw err;
        } finally {
            setCarregando(false);
        }
    }, [estado.jogoId, estado.jogadorAtual, atualizarEstado]);
    
    /**
     * Compra bilhetes de destino
     */
    const comprarBilhetes = useCallback(async (
        bilhetesEscolhidos: string[],
        bilhetesDescartados: string[]
    ) => {
        if (!estado.jogoId || !estado.jogadorAtual) return;
        
        setCarregando(true);
        setErro(null);
        
        try {
            await gameApi.comprarBilhetes(estado.jogoId, {
                jogador_id: estado.jogadorAtual,
                bilhetes_escolhidos: bilhetesEscolhidos,
                bilhetes_descartados: bilhetesDescartados,
            });
            
            await atualizarEstado();
        } catch (err: any) {
            setErro(err.message);
            throw err;
        } finally {
            setCarregando(false);
        }
    }, [estado.jogoId, estado.jogadorAtual, atualizarEstado]);
    
    /**
     * Finaliza turno do jogador
     */
    const finalizarTurno = useCallback(async () => {
        if (!estado.jogoId || !estado.jogadorAtual) return;
        
        setCarregando(true);
        setErro(null);
        
        try {
            await gameApi.finalizarTurno(estado.jogoId, {
                jogador_id: estado.jogadorAtual,
            });
            
            await atualizarEstado();
        } catch (err: any) {
            setErro(err.message);
            throw err;
        } finally {
            setCarregando(false);
        }
    }, [estado.jogoId, estado.jogadorAtual, atualizarEstado]);
    
    /**
     * Obtém mão de cartas do jogador atual
     */
    const obterMao = useCallback(async (): Promise<CartaVagao[]> => {
        if (!estado.jogoId || !estado.jogadorAtual) return [];
        
        try {
            const response = await gameApi.obterMaoJogador(estado.jogoId, estado.jogadorAtual);
            return response.cartas;
        } catch (err: any) {
            setErro(err.message);
            return [];
        }
    }, [estado.jogoId, estado.jogadorAtual]);
    
    /**
     * Obtém bilhetes do jogador atual
     */
    const obterBilhetes = useCallback(async (): Promise<BilheteDestino[]> => {
        if (!estado.jogoId || !estado.jogadorAtual) return [];
        
        try {
            const response = await gameApi.obterBilhetesJogador(estado.jogoId, estado.jogadorAtual);
            return response.bilhetes;
        } catch (err: any) {
            setErro(err.message);
            return [];
        }
    }, [estado.jogoId, estado.jogadorAtual]);
    
    /**
     * Obtém placar de todos os jogadores
     */
    const obterPlacar = useCallback(async (): Promise<JogadorPlacar[]> => {
        if (!estado.jogoId) return [];
        
        try {
            const response = await gameApi.obterPlacar(estado.jogoId);
            return response.jogadores;
        } catch (err: any) {
            setErro(err.message);
            return [];
        }
    }, [estado.jogoId]);
    
    /**
     * Obtém contador de trens de todos os jogadores
     */
    const obterTrens = useCallback(async (): Promise<JogadorTrens[]> => {
        if (!estado.jogoId) return [];
        
        try {
            const response = await gameApi.obterEstadoJogo(estado.jogoId);
            return response.jogadores.map((j: any) => ({
                id: j.id,
                nome: j.nome,
                trensRestantes: j.trensRestantes,
                cor: j.cor,
            }));
        } catch (err: any) {
            setErro(err.message);
            return [];
        }
    }, [estado.jogoId]);
    
    /**
     * Limpa mensagem de erro
     */
    const limparErro = useCallback(() => {
        setErro(null);
    }, []);
    
    // Polling automático para atualizar estado (a cada 3 segundos)
    useEffect(() => {
        if (estado.jogoId && estado.fase === 'jogando') {
            const interval = setInterval(() => {
                atualizarEstado();
            }, 3000);
            
            return () => clearInterval(interval);
        }
    }, [estado.jogoId, estado.fase, atualizarEstado]);
    
    const value: GameContextType = {
        estado,
        carregando,
        erro,
        criarJogo,
        comprarCartas,
        conquistarRota,
        comprarBilhetes,
        finalizarTurno,
        atualizarEstado,
        obterMao,
        obterBilhetes,
        obterPlacar,
        obterTrens,
        limparErro,
    };
    
    return (
        <GameContext.Provider value={value}>
            {children}
        </GameContext.Provider>
    );
}

/**
 * Hook para usar o Context do Jogo
 * 
 * GRASP - Indirection:
 * Componentes acessam estado via este hook, não diretamente
 */
export function useGame() {
    const context = useContext(GameContext);
    
    if (!context) {
        throw new Error('useGame deve ser usado dentro de GameProvider');
    }
    
    return context;
}
