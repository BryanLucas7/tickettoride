/**
 * COMPONENTE: Mão de Cartas do Jogador
 * =====================================
 * 
 * Exibe todas as cartas de vagão que o jogador possui, agrupadas por cor.
 * Permite visualização expandida/recolhida.
 * 
 * GRASP Principles:
 * - Information Expert: Recebe dados de Mao (que gerencia cartas)
 * - High Cohesion: Focado apenas em exibir mão de cartas
 * - Low Coupling: Não conhece lógica de jogo, apenas apresenta dados
 */

'use client';

import { useState } from 'react';

export enum CorCarta {
    VERMELHO = 'VERMELHO',
    AZUL = 'AZUL',
    VERDE = 'VERDE',
    AMARELO = 'AMARELO',
    LARANJA = 'LARANJA',
    BRANCO = 'BRANCO',
    PRETO = 'PRETO',
    ROXO = 'ROXO',
    LOCOMOTIVA = 'LOCOMOTIVA'
}

export interface CartaVagao {
    cor: CorCarta;
    id?: string;
}

export interface MaoCartasProps {
    cartas: CartaVagao[];
    jogadorNome: string;
    isExpanded?: boolean;
    onCartaSelecionada?: (carta: CartaVagao) => void;
    cartasSelecionadas?: CartaVagao[];
    modoSelecao?: boolean;
}

interface CartasAgrupadas {
    [key: string]: CartaVagao[];
}

export default function MaoCartas({
    cartas,
    jogadorNome,
    isExpanded: initialExpanded = false,
    onCartaSelecionada,
    cartasSelecionadas = [],
    modoSelecao = false
}: MaoCartasProps) {
    const [isExpanded, setIsExpanded] = useState(initialExpanded);
    
    /**
     * Information Expert: Agrupa cartas por cor
     * Lógica de apresentação isolada no componente
     */
    
    /**
     * Normaliza cor da API (lowercase) para enum (UPPERCASE)
     */
    const normalizarCor = (cor: string): CorCarta => {
        return cor.toUpperCase() as CorCarta;
    };
    
    const agruparCartasPorCor = (): CartasAgrupadas => {
        return cartas.reduce((grupos, carta) => {
            const cor = normalizarCor(carta.cor); // Normaliza para UPPERCASE
            if (!grupos[cor]) {
                grupos[cor] = [];
            }
            grupos[cor].push({ ...carta, cor }); // Atualiza com cor normalizada
            return grupos;
        }, {} as CartasAgrupadas);
    };
    
    /**
     * Retorna configuração visual para cada cor
     */
    const getCorConfig = (cor: CorCarta) => {
        const configs = {
            [CorCarta.VERMELHO]: {
                bg: 'bg-red-500',
                border: 'border-red-700',
                text: 'text-white',
                label: 'Vermelho',
                emoji: '🔴'
            },
            [CorCarta.AZUL]: {
                bg: 'bg-blue-500',
                border: 'border-blue-700',
                text: 'text-white',
                label: 'Azul',
                emoji: '🔵'
            },
            [CorCarta.VERDE]: {
                bg: 'bg-green-500',
                border: 'border-green-700',
                text: 'text-white',
                label: 'Verde',
                emoji: '🟢'
            },
            [CorCarta.AMARELO]: {
                bg: 'bg-yellow-400',
                border: 'border-yellow-600',
                text: 'text-gray-900',
                label: 'Amarelo',
                emoji: '🟡'
            },
            [CorCarta.LARANJA]: {
                bg: 'bg-orange-500',
                border: 'border-orange-700',
                text: 'text-white',
                label: 'Laranja',
                emoji: '🟠'
            },
            [CorCarta.BRANCO]: {
                bg: 'bg-gray-100',
                border: 'border-gray-400',
                text: 'text-gray-900',
                label: 'Branco',
                emoji: '⚪'
            },
            [CorCarta.PRETO]: {
                bg: 'bg-gray-900',
                border: 'border-gray-700',
                text: 'text-white',
                label: 'Preto',
                emoji: '⚫'
            },
            [CorCarta.ROXO]: {
                bg: 'bg-purple-500',
                border: 'border-purple-700',
                text: 'text-white',
                label: 'Roxo',
                emoji: '🟣'
            },
            [CorCarta.LOCOMOTIVA]: {
                bg: 'bg-gradient-to-br from-purple-600 to-pink-600',
                border: 'border-purple-800',
                text: 'text-white',
                label: 'Locomotiva',
                emoji: '🚂'
            }
        };
        
        return configs[cor];
    };
    
    /**
     * Verifica se carta está selecionada
     */
    const isCartaSelecionada = (carta: CartaVagao): boolean => {
        return cartasSelecionadas.some(c => c.id === carta.id);
    };
    
    /**
     * Handler para clique em carta
     */
    const handleCartaClick = (carta: CartaVagao) => {
        if (modoSelecao && onCartaSelecionada) {
            onCartaSelecionada(carta);
        }
    };
    
    const cartasAgrupadas = agruparCartasPorCor();
    const totalCartas = cartas.length;
    const cores = Object.keys(cartasAgrupadas).sort();
    
    return (
        <div className="bg-white rounded-lg shadow-lg border-2 border-gray-200 overflow-hidden">
            {/* Header */}
            <div 
                className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 cursor-pointer hover:from-blue-700 hover:to-indigo-700 transition-colors"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <span className="text-3xl">🎴</span>
                        <div>
                            <h3 className="text-white font-bold text-lg">
                                Mão de {jogadorNome}
                            </h3>
                            <p className="text-blue-100 text-sm">
                                {totalCartas} {totalCartas === 1 ? 'carta' : 'cartas'}
                            </p>
                        </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                        {!isExpanded && (
                            <div className="flex space-x-1">
                                {cores.slice(0, 5).map(cor => {
                                    const config = getCorConfig(cor as CorCarta);
                                    return (
                                        <div
                                            key={cor}
                                            className={`w-8 h-8 rounded-full ${config.bg} border-2 ${config.border} flex items-center justify-center text-xs font-bold ${config.text}`}
                                        >
                                            {cartasAgrupadas[cor].length}
                                        </div>
                                    );
                                })}
                                {cores.length > 5 && (
                                    <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-xs font-bold">
                                        +{cores.length - 5}
                                    </div>
                                )}
                            </div>
                        )}
                        
                        <button className="text-white text-2xl transition-transform duration-200" style={{
                            transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)'
                        }}>
                            ▼
                        </button>
                    </div>
                </div>
            </div>
            
            {/* Conteúdo Expandido */}
            {isExpanded && (
                <div className="p-4 space-y-3">
                    {cores.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            <p className="text-lg">Nenhuma carta na mão</p>
                            <p className="text-sm">Compre cartas para começar!</p>
                        </div>
                    ) : (
                        cores.map(cor => {
                            const config = getCorConfig(cor as CorCarta);
                            const cartasDaCor = cartasAgrupadas[cor];
                            
                            return (
                                <div key={cor} className="border-2 border-gray-200 rounded-lg p-3">
                                    {/* Header do Grupo */}
                                    <div className="flex items-center justify-between mb-2">
                                        <div className="flex items-center space-x-2">
                                            <span className="text-2xl">{config.emoji}</span>
                                            <span className="font-bold text-gray-800">
                                                {config.label}
                                            </span>
                                        </div>
                                        <span className="bg-gray-200 px-3 py-1 rounded-full text-sm font-semibold">
                                            {cartasDaCor.length} {cartasDaCor.length === 1 ? 'carta' : 'cartas'}
                                        </span>
                                    </div>
                                    
                                    {/* Cartas do Grupo */}
                                    <div className="flex flex-wrap gap-2">
                                        {cartasDaCor.map((carta, index) => {
                                            const selecionada = isCartaSelecionada(carta);
                                            
                                            return (
                                                <div
                                                    key={carta.id || `${cor}-${index}`}
                                                    onClick={() => handleCartaClick(carta)}
                                                    className={`
                                                        relative w-16 h-24 rounded-lg ${config.bg} border-4 ${config.border}
                                                        flex flex-col items-center justify-center
                                                        transition-all duration-200 transform
                                                        ${modoSelecao ? 'cursor-pointer hover:scale-110 hover:shadow-lg' : ''}
                                                        ${selecionada ? 'scale-110 ring-4 ring-yellow-400 shadow-xl' : ''}
                                                    `}
                                                >
                                                    {/* Ícone da Carta */}
                                                    <span className="text-3xl mb-1">{config.emoji}</span>
                                                    
                                                    {/* Tipo da Carta */}
                                                    <span className={`text-xs font-bold ${config.text} text-center px-1`}>
                                                        {cor === CorCarta.LOCOMOTIVA ? '🚂' : 'Vagão'}
                                                    </span>
                                                    
                                                    {/* Indicador de Seleção */}
                                                    {selecionada && (
                                                        <div className="absolute -top-2 -right-2 bg-yellow-400 rounded-full w-6 h-6 flex items-center justify-center border-2 border-yellow-600">
                                                            <span className="text-xs font-bold">✓</span>
                                                        </div>
                                                    )}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        })
                    )}
                    
                    {/* Resumo */}
                    {totalCartas > 0 && (
                        <div className="border-t-2 border-gray-200 pt-3 mt-3">
                            <div className="grid grid-cols-2 gap-2 text-sm">
                                <div className="bg-gray-50 p-2 rounded">
                                    <span className="text-gray-600">Total de Cartas:</span>
                                    <span className="font-bold ml-2">{totalCartas}</span>
                                </div>
                                <div className="bg-gray-50 p-2 rounded">
                                    <span className="text-gray-600">Cores Diferentes:</span>
                                    <span className="font-bold ml-2">{cores.length}</span>
                                </div>
                            </div>
                            
                            {modoSelecao && (
                                <div className="mt-2 bg-blue-50 border-l-4 border-blue-500 p-2 text-sm text-blue-800">
                                    💡 Clique nas cartas para selecioná-las ({cartasSelecionadas.length} selecionadas)
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
