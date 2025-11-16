/**
 * CONTADOR DE TRENS RESTANTES - Componente UI
 * ============================================
 * 
 * Exibe quantidade de trens restantes de cada jogador.
 * Alerta visual quando jogador tem ≤2 trens (fim de jogo iminente).
 * 
 * Princípios GRASP aplicados:
 * - Information Expert: Jogador possui e gerencia seus trens
 * - High Cohesion: Componente focado apenas em exibir contadores de trens
 * - Low Coupling: Não conhece lógica de conquista de rotas
 * 
 * Padrão GoF: Observer Pattern - Observa mudanças no número de trens
 */

'use client';

import { useState, useEffect } from 'react';

/**
 * Interface do Jogador para contador de trens
 */
export interface JogadorTrens {
    id: string;
    nome: string;
    trensRestantes: number;
    cor: string; // Cor visual do jogador
}

/**
 * Props do Componente
 */
interface ContadorTrensProps {
    jogadores: JogadorTrens[];
    trensIniciais?: number;      // Quantidade inicial de trens (padrão: 45)
    limiteAlerta?: number;       // Alerta quando trens <= este valor (padrão: 2)
    modo?: 'compacto' | 'expandido'; // Modo de visualização
    mostrarBarras?: boolean;     // Mostra barras de progresso
    animarMudancas?: boolean;    // Anima mudanças
}

/**
 * Mapa de cores CSS
 */
const CORES_JOGADORES: Record<string, { bg: string, text: string, border: string }> = {
    red: { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-500' },
    blue: { bg: 'bg-blue-100', text: 'text-blue-800', border: 'border-blue-500' },
    green: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-500' },
    yellow: { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-500' },
    purple: { bg: 'bg-purple-100', text: 'text-purple-800', border: 'border-purple-500' },
    orange: { bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-500' },
    pink: { bg: 'bg-pink-100', text: 'text-pink-800', border: 'border-pink-500' },
    teal: { bg: 'bg-teal-100', text: 'text-teal-800', border: 'border-teal-500' },
};

/**
 * Componente Principal
 * 
 * GRASP - Information Expert:
 * Jogador conhece seus trens, componente apresenta essa informação
 * 
 * GRASP - High Cohesion:
 * Focado apenas em exibir contador de trens
 * 
 * Observer Pattern:
 * Reage a mudanças no número de trens dos jogadores
 */
export default function ContadorTrens({
    jogadores,
    trensIniciais = 45,
    limiteAlerta = 2,
    modo = 'expandido',
    mostrarBarras = true,
    animarMudancas = true
}: ContadorTrensProps) {
    const [jogadoresAnteriores, setJogadoresAnteriores] = useState(jogadores);
    const [mudancas, setMudancas] = useState<Record<string, number>>({});
    const [alertaFimJogo, setAlertaFimJogo] = useState(false);
    
    /**
     * Observer Pattern:
     * Detecta mudanças no número de trens e registra para animação
     */
    useEffect(() => {
        if (!animarMudancas) return;
        
        const novasMudancas: Record<string, number> = {};
        let temAlerta = false;
        
        jogadores.forEach(jogador => {
            const anterior = jogadoresAnteriores.find(j => j.id === jogador.id);
            
            if (anterior && anterior.trensRestantes !== jogador.trensRestantes) {
                novasMudancas[jogador.id] = jogador.trensRestantes - anterior.trensRestantes;
            }
            
            // Verifica alerta de fim de jogo
            if (jogador.trensRestantes <= limiteAlerta) {
                temAlerta = true;
            }
        });
        
        if (Object.keys(novasMudancas).length > 0) {
            setMudancas(novasMudancas);
            
            // Remove indicadores após 2 segundos
            setTimeout(() => {
                setMudancas({});
            }, 2000);
        }
        
        setAlertaFimJogo(temAlerta);
        setJogadoresAnteriores(jogadores);
    }, [jogadores, animarMudancas, limiteAlerta, jogadoresAnteriores]);
    
    if (modo === 'compacto') {
        return (
            <ModoCompacto
                jogadores={jogadores}
                limiteAlerta={limiteAlerta}
                mudancas={mudancas}
            />
        );
    }
    
    return (
        <ModoExpandido
            jogadores={jogadores}
            trensIniciais={trensIniciais}
            limiteAlerta={limiteAlerta}
            mostrarBarras={mostrarBarras}
            mudancas={mudancas}
            alertaFimJogo={alertaFimJogo}
        />
    );
}

/**
 * Modo Expandido
 * 
 * GRASP - High Cohesion: Focado em exibir detalhes completos
 */
function ModoExpandido({
    jogadores,
    trensIniciais,
    limiteAlerta,
    mostrarBarras,
    mudancas,
    alertaFimJogo
}: {
    jogadores: JogadorTrens[];
    trensIniciais: number;
    limiteAlerta: number;
    mostrarBarras: boolean;
    mudancas: Record<string, number>;
    alertaFimJogo: boolean;
}) {
    const jogadorComMenosTrens = [...jogadores].sort((a, b) => a.trensRestantes - b.trensRestantes)[0];
    
    return (
        <div className="bg-gradient-to-br from-amber-50 to-orange-100 rounded-lg shadow-lg border-2 border-amber-300 p-4">
            {/* Cabeçalho */}
            <div className="flex items-center gap-2 mb-4 pb-3 border-b-2 border-amber-300">
                <span className="text-3xl">🚂</span>
                <div className="flex-1">
                    <h3 className="font-bold text-lg text-amber-900">Trens Restantes</h3>
                    <p className="text-sm text-amber-700">
                        Inicial: {trensIniciais} trens por jogador
                    </p>
                </div>
                
                {alertaFimJogo && (
                    <div className="bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold animate-pulse">
                        ⚠️ FIM PRÓXIMO
                    </div>
                )}
            </div>
            
            {/* Lista de jogadores */}
            <div className="space-y-3">
                {jogadores.map(jogador => {
                    const mudanca = mudancas[jogador.id];
                    const porcentagem = (jogador.trensRestantes / trensIniciais) * 100;
                    const cores = CORES_JOGADORES[jogador.cor] || CORES_JOGADORES.blue;
                    const emAlerta = jogador.trensRestantes <= limiteAlerta;
                    
                    return (
                        <div
                            key={jogador.id}
                            className={`
                                rounded-lg p-3 border-2 transition-all
                                ${emAlerta 
                                    ? 'bg-red-50 border-red-500 shadow-lg animate-pulse' 
                                    : `${cores.bg} ${cores.border}`
                                }
                            `}
                        >
                            <div className="flex items-center justify-between mb-2">
                                {/* Nome e ícone */}
                                <div className="flex items-center gap-2">
                                    <span className="text-2xl">🚂</span>
                                    <span className={`font-bold ${emAlerta ? 'text-red-800' : cores.text}`}>
                                        {jogador.nome}
                                    </span>
                                    
                                    {emAlerta && (
                                        <span className="bg-red-500 text-white px-2 py-0.5 rounded text-xs font-bold">
                                            ALERTA
                                        </span>
                                    )}
                                </div>
                                
                                {/* Contador */}
                                <div className="flex items-center gap-2">
                                    <span className={`text-2xl font-bold ${emAlerta ? 'text-red-700' : cores.text}`}>
                                        {jogador.trensRestantes}
                                    </span>
                                    <span className="text-sm text-gray-600">trens</span>
                                    
                                    {/* Indicador de mudança */}
                                    {mudanca !== undefined && mudanca !== 0 && (
                                        <span className={`
                                            text-xs font-bold px-2 py-1 rounded-full
                                            ${mudanca < 0 
                                                ? 'bg-orange-100 text-orange-700' 
                                                : 'bg-blue-100 text-blue-700'
                                            }
                                            animate-bounce
                                        `}>
                                            {mudanca > 0 ? '+' : ''}{mudanca}
                                        </span>
                                    )}
                                </div>
                            </div>
                            
                            {/* Barra de progresso */}
                            {mostrarBarras && (
                                <>
                                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                        <div
                                            className={`
                                                h-full transition-all duration-500
                                                ${emAlerta ? 'bg-red-500' : cores.border.replace('border-', 'bg-')}
                                            `}
                                            style={{ width: `${porcentagem}%` }}
                                        />
                                    </div>
                                    
                                    <div className="flex justify-between items-center mt-1">
                                        <span className="text-xs text-gray-500">
                                            {porcentagem.toFixed(0)}% restante
                                        </span>
                                        
                                        <span className="text-xs text-gray-500">
                                            Usados: {trensIniciais - jogador.trensRestantes}
                                        </span>
                                    </div>
                                </>
                            )}
                            
                            {/* Mensagem de alerta */}
                            {emAlerta && (
                                <div className="mt-2 bg-red-100 border-l-4 border-red-500 p-2 rounded">
                                    <p className="text-xs text-red-800 font-semibold">
                                        ⚠️ Última rodada! Este jogador tem ≤{limiteAlerta} trens.
                                    </p>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
            
            {/* Resumo */}
            <div className="mt-4 pt-3 border-t-2 border-amber-300">
                <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="bg-white rounded p-2">
                        <div className="text-xs text-gray-600">Jogador com Menos Trens</div>
                        <div className="font-bold text-gray-800">
                            {jogadorComMenosTrens?.nome} ({jogadorComMenosTrens?.trensRestantes})
                        </div>
                    </div>
                    
                    <div className="bg-white rounded p-2">
                        <div className="text-xs text-gray-600">Total de Jogadores</div>
                        <div className="font-bold text-gray-800">{jogadores.length}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

/**
 * Modo Compacto
 * 
 * GRASP - High Cohesion: Versão resumida para economizar espaço
 */
function ModoCompacto({
    jogadores,
    limiteAlerta,
    mudancas
}: {
    jogadores: JogadorTrens[];
    limiteAlerta: number;
    mudancas: Record<string, number>;
}) {
    return (
        <div className="bg-amber-100 rounded-lg border-2 border-amber-300 p-3">
            <div className="flex items-center gap-2 mb-2">
                <span className="text-xl">🚂</span>
                <span className="font-bold text-sm text-amber-900">Trens</span>
            </div>
            
            <div className="space-y-1">
                {jogadores.map(jogador => {
                    const mudanca = mudancas[jogador.id];
                    const emAlerta = jogador.trensRestantes <= limiteAlerta;
                    const cores = CORES_JOGADORES[jogador.cor] || CORES_JOGADORES.blue;
                    
                    return (
                        <div
                            key={jogador.id}
                            className={`
                                flex items-center justify-between p-2 rounded
                                ${emAlerta ? 'bg-red-100 animate-pulse' : 'bg-white'}
                            `}
                        >
                            <span className={`text-sm font-semibold ${emAlerta ? 'text-red-800' : cores.text}`}>
                                {jogador.nome}
                            </span>
                            
                            <div className="flex items-center gap-1">
                                <span className={`font-bold ${emAlerta ? 'text-red-700' : 'text-gray-800'}`}>
                                    {jogador.trensRestantes}
                                </span>
                                
                                {emAlerta && <span className="text-red-500">⚠️</span>}
                                
                                {mudanca !== undefined && mudanca !== 0 && (
                                    <span className="text-xs text-orange-600">
                                        ({mudanca > 0 ? '+' : ''}{mudanca})
                                    </span>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
