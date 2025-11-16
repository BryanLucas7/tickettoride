/**
 * PAINEL DE BILHETES DE DESTINO - Componente UI
 * ===============================================
 * 
 * Exibe os bilhetes de destino secretos do jogador com informações de:
 * - Origem e destino
 * - Pontos do bilhete
 * - Status de conclusão (completo/incompleto)
 * 
 * Princípios GRASP aplicados:
 * - Information Expert: Jogador possui bilhetes e conhece seus destinos
 * - Protected Variations: Bilhetes são secretos até o fim do jogo
 * - High Cohesion: Componente focado apenas em exibir bilhetes
 * - Low Coupling: Não contém lógica de jogo, apenas apresentação
 * 
 * Padrão GoF: Observer Pattern - Reagirá a mudanças no status de bilhetes
 */

'use client';

import { useState } from 'react';

/**
 * Interface do Bilhete de Destino
 */
export interface BilheteDestino {
    id: string;
    origem: string;
    destino: string;
    pontos: number;
    completo: boolean; // true = jogador conectou origem-destino
}

/**
 * Props do Componente
 */
interface PainelBilhetesDestinoProps {
    bilhetes: BilheteDestino[];
    jogadorNome: string;
    modoSecreto?: boolean; // Se true, esconde de outros jogadores
    isExpanded?: boolean;   // Controla expansão inicial
    mostrarStatus?: boolean; // Mostra indicadores de completo/incompleto
}

/**
 * Componente Principal
 * 
 * GRASP - Information Expert: 
 * Recebe dados de bilhetes do jogador e apresenta informações relevantes
 * 
 * GRASP - High Cohesion:
 * Focado apenas em exibir bilhetes de destino, não mistura outras responsabilidades
 * 
 * GRASP - Low Coupling:
 * Não conhece lógica de jogo ou regras de validação, apenas apresenta dados
 */
export default function PainelBilhetesDestino({
    bilhetes,
    jogadorNome,
    modoSecreto = true,
    isExpanded = true,
    mostrarStatus = true
}: PainelBilhetesDestinoProps) {
    const [expandido, setExpandido] = useState(isExpanded);
    
    // Estatísticas dos bilhetes
    const totalBilhetes = bilhetes.length;
    const bilhetesCompletos = bilhetes.filter(b => b.completo).length;
    const bilhetesIncompletos = totalBilhetes - bilhetesCompletos;
    const pontosGanhos = bilhetes
        .filter(b => b.completo)
        .reduce((total, b) => total + b.pontos, 0);
    const pontosPerdidos = bilhetes
        .filter(b => !b.completo)
        .reduce((total, b) => total + b.pontos, 0);
    const pontosTotaisPossiveis = bilhetes.reduce((total, b) => total + b.pontos, 0);
    
    /**
     * GRASP - Protected Variations:
     * Se modo secreto ativado, esconde detalhes dos bilhetes
     */
    if (modoSecreto && bilhetes.length > 0) {
        return (
            <div className="bg-gradient-to-br from-amber-50 to-yellow-100 rounded-lg shadow-md p-4 border-2 border-amber-300">
                <div className="flex items-center gap-2">
                    <span className="text-2xl">🎫</span>
                    <div>
                        <h3 className="font-bold text-amber-900">Bilhetes de Destino</h3>
                        <p className="text-sm text-amber-700">
                            {jogadorNome} possui {totalBilhetes} bilhetes secretos
                        </p>
                    </div>
                    <div className="ml-auto">
                        <span className="text-3xl">🔒</span>
                    </div>
                </div>
            </div>
        );
    }
    
    return (
        <div className="bg-gradient-to-br from-purple-50 to-indigo-100 rounded-lg shadow-lg border-2 border-purple-300">
            {/* Cabeçalho */}
            <div
                className="flex items-center justify-between p-4 cursor-pointer hover:bg-purple-100 transition-colors rounded-t-lg"
                onClick={() => setExpandido(!expandido)}
            >
                <div className="flex items-center gap-3">
                    <span className="text-3xl">🎫</span>
                    <div>
                        <h3 className="font-bold text-lg text-purple-900">
                            Bilhetes de Destino - {jogadorNome}
                        </h3>
                        <p className="text-sm text-purple-700">
                            {totalBilhetes} bilhetes | {bilhetesCompletos} completos
                        </p>
                    </div>
                </div>
                
                <div className="flex items-center gap-2">
                    {/* Indicador de pontos */}
                    <div className="text-right mr-2">
                        <div className="text-sm font-semibold text-green-600">
                            +{pontosGanhos} pts
                        </div>
                        {pontosPerdidos > 0 && (
                            <div className="text-xs font-semibold text-red-600">
                                -{pontosPerdidos} pts
                            </div>
                        )}
                    </div>
                    
                    {/* Seta de expansão */}
                    <span className={`text-2xl transition-transform ${expandido ? 'rotate-180' : ''}`}>
                        ▼
                    </span>
                </div>
            </div>
            
            {/* Conteúdo expandido */}
            {expandido && (
                <div className="p-4 pt-0">
                    {bilhetes.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            <span className="text-4xl block mb-2">🎫</span>
                            <p>Nenhum bilhete de destino</p>
                        </div>
                    ) : (
                        <>
                            {/* Lista de bilhetes */}
                            <div className="space-y-3 mb-4">
                                {bilhetes.map((bilhete) => (
                                    <BilheteCard
                                        key={bilhete.id}
                                        bilhete={bilhete}
                                        mostrarStatus={mostrarStatus}
                                    />
                                ))}
                            </div>
                            
                            {/* Resumo estatístico */}
                            <div className="bg-white rounded-lg p-4 shadow-inner">
                                <h4 className="font-bold text-sm text-gray-700 mb-3">
                                    📊 Resumo
                                </h4>
                                
                                <div className="grid grid-cols-2 gap-3">
                                    <div className="bg-green-50 rounded p-2 border-l-4 border-green-500">
                                        <div className="text-xs text-green-700">Completos</div>
                                        <div className="font-bold text-green-800">
                                            {bilhetesCompletos} bilhetes
                                        </div>
                                        <div className="text-sm text-green-600">
                                            +{pontosGanhos} pontos
                                        </div>
                                    </div>
                                    
                                    <div className="bg-red-50 rounded p-2 border-l-4 border-red-500">
                                        <div className="text-xs text-red-700">Incompletos</div>
                                        <div className="font-bold text-red-800">
                                            {bilhetesIncompletos} bilhetes
                                        </div>
                                        <div className="text-sm text-red-600">
                                            -{pontosPerdidos} pontos
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="mt-3 pt-3 border-t border-gray-200">
                                    <div className="flex justify-between items-center">
                                        <span className="text-sm font-semibold text-gray-700">
                                            Balanço Total:
                                        </span>
                                        <span className={`text-lg font-bold ${
                                            (pontosGanhos - pontosPerdidos) >= 0 
                                                ? 'text-green-600' 
                                                : 'text-red-600'
                                        }`}>
                                            {pontosGanhos - pontosPerdidos > 0 ? '+' : ''}
                                            {pontosGanhos - pontosPerdidos} pts
                                        </span>
                                    </div>
                                    
                                    <div className="flex justify-between items-center mt-1">
                                        <span className="text-xs text-gray-500">
                                            Pontos possíveis:
                                        </span>
                                        <span className="text-sm text-gray-600">
                                            {pontosTotaisPossiveis} pts
                                        </span>
                                    </div>
                                    
                                    {/* Barra de progresso */}
                                    <div className="mt-2">
                                        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                            <div
                                                className="h-full bg-gradient-to-r from-green-500 to-green-600 transition-all"
                                                style={{
                                                    width: `${totalBilhetes > 0 
                                                        ? (bilhetesCompletos / totalBilhetes) * 100 
                                                        : 0}%`
                                                }}
                                            />
                                        </div>
                                        <div className="text-xs text-center text-gray-500 mt-1">
                                            {totalBilhetes > 0 
                                                ? Math.round((bilhetesCompletos / totalBilhetes) * 100)
                                                : 0}% completo
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    );
}

/**
 * Componente de Card Individual de Bilhete
 * 
 * GRASP - High Cohesion: Responsável apenas por exibir um bilhete
 */
function BilheteCard({ 
    bilhete, 
    mostrarStatus 
}: { 
    bilhete: BilheteDestino; 
    mostrarStatus: boolean;
}) {
    const { origem, destino, pontos, completo } = bilhete;
    
    return (
        <div className={`
            rounded-lg p-3 border-2 transition-all
            ${completo 
                ? 'bg-green-50 border-green-400 shadow-sm' 
                : 'bg-white border-purple-300 shadow-md'
            }
        `}>
            <div className="flex items-center justify-between">
                {/* Origem e Destino */}
                <div className="flex items-center gap-2 flex-1">
                    <span className="font-bold text-purple-900 text-sm">
                        {origem}
                    </span>
                    <span className="text-2xl">
                        {completo ? '✅' : '➡️'}
                    </span>
                    <span className="font-bold text-purple-900 text-sm">
                        {destino}
                    </span>
                </div>
                
                {/* Pontos */}
                <div className={`
                    px-3 py-1 rounded-full font-bold text-sm
                    ${completo 
                        ? 'bg-green-200 text-green-800' 
                        : 'bg-purple-200 text-purple-800'
                    }
                `}>
                    {completo ? '+' : ''}{pontos} pts
                </div>
            </div>
            
            {/* Status visual */}
            {mostrarStatus && (
                <div className="mt-2 text-xs flex items-center gap-2">
                    {completo ? (
                        <>
                            <span className="text-green-600">●</span>
                            <span className="text-green-700 font-semibold">
                                Bilhete completo - Pontos garantidos!
                            </span>
                        </>
                    ) : (
                        <>
                            <span className="text-orange-500">●</span>
                            <span className="text-orange-700">
                                Conecte {origem} ↔ {destino} para ganhar {pontos} pontos
                            </span>
                        </>
                    )}
                </div>
            )}
        </div>
    );
}
