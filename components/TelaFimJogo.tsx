/**
 * TELA DE FIM DE JOGO E RESULTADOS - Componente UI
 * =================================================
 * 
 * Exibe pontuação final detalhada de cada jogador ao fim da partida:
 * - Pontos de rotas conquistadas
 * - Bilhetes de destino completos (+pontos)
 * - Bilhetes de destino incompletos (-pontos)
 * - Bônus de maior caminho contínuo (+10 pontos)
 * - Pontuação total
 * - Destaque do vencedor
 * 
 * Princípios GRASP aplicados:
 * - Information Expert: Placar calcula pontuação final
 * - High Cohesion: Componente focado apenas em exibir resultados
 * - Low Coupling: Recebe dados prontos, não calcula pontos
 * 
 * Padrão GoF: Observer Pattern - Ativado quando jogo termina
 */

'use client';

import { useState } from 'react';

/**
 * Interface de Bilhete para resultados
 */
export interface BilheteResultado {
    origem: string;
    destino: string;
    pontos: number;
    completo: boolean;
}

/**
 * Interface de Pontuação Final de um Jogador
 */
export interface PontuacaoFinal {
    jogadorId: string;
    jogadorNome: string;
    jogadorCor: string;
    pontosRotas: number;           // Pontos de rotas conquistadas
    bilhetesCompletos: BilheteResultado[];
    bilhetesIncompletos: BilheteResultado[];
    pontosBilhetesPositivos: number;  // Soma de bilhetes completos
    pontosBilhetesNegativos: number;  // Soma de bilhetes incompletos (já negativo)
    bonusMaiorCaminho: boolean;    // true = ganhou bônus de +10
    pontosMaiorCaminho: number;    // 10 ou 0
    pontuacaoTotal: number;        // Soma de tudo
    tamanhoMaiorCaminho?: number;  // Tamanho do maior caminho (opcional)
}

/**
 * Props do Componente
 */
interface TelaFimJogoProps {
    pontuacoes: PontuacaoFinal[];
    exibir: boolean;               // Controla visibilidade
    onJogarNovamente?: () => void; // Callback para novo jogo
    onVoltarMenu?: () => void;     // Callback para voltar ao menu
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
    black: { bg: 'bg-gray-900', text: 'text-white', border: 'border-gray-700' },
    white: { bg: 'bg-white', text: 'text-gray-800', border: 'border-gray-300' },
};

/**
 * Componente Principal
 * 
 * GRASP - Information Expert:
 * Placar (backend) calcula todos os pontos. UI apenas apresenta resultados.
 * 
 * GRASP - High Cohesion:
 * Focado exclusivamente em exibir resultados finais de jogo.
 * 
 * GRASP - Low Coupling:
 * Não conhece lógica de cálculo de pontos, apenas recebe e exibe.
 */
export default function TelaFimJogo({
    pontuacoes,
    exibir,
    onJogarNovamente,
    onVoltarMenu
}: TelaFimJogoProps) {
    const [mostrarDetalhes, setMostrarDetalhes] = useState<Record<string, boolean>>({});
    
    if (!exibir) return null;
    
    // Ordena jogadores por pontuação (maior para menor)
    const pontuacoesOrdenadas = [...pontuacoes].sort((a, b) => b.pontuacaoTotal - a.pontuacaoTotal);
    const vencedor = pontuacoesOrdenadas[0];
    
    // Verifica empate
    const empate = pontuacoesOrdenadas.filter(p => p.pontuacaoTotal === vencedor.pontuacaoTotal).length > 1;

    // Layout dinâmico do pódio (até 5 jogadores)
    const PODIO_STYLES = [
        { medalha: '🥇', fundo: 'bg-gradient-to-b from-yellow-400 to-yellow-600', borda: 'border-yellow-600', largura: 'w-28' },
        { medalha: '🥈', fundo: 'bg-gradient-to-b from-gray-300 to-gray-500', borda: 'border-gray-600', largura: 'w-28' },
        { medalha: '🥉', fundo: 'bg-gradient-to-b from-amber-600 to-amber-800', borda: 'border-amber-900', largura: 'w-28' }
    ];
    const estiloPadrao = {
        medalha: '🏅',
        fundo: 'bg-gradient-to-b from-gray-200 to-gray-300',
        borda: 'border-gray-400',
        largura: 'w-24'
    };
    const podioJogadores = pontuacoesOrdenadas.slice(0, Math.min(5, pontuacoesOrdenadas.length));
    const pontosPodio = podioJogadores.map((p) => p.pontuacaoTotal);
    const maxPontuacao = pontosPodio.length ? Math.max(...pontosPodio) : 0;
    const minPontuacao = pontosPodio.length ? Math.min(...pontosPodio) : 0;
    const faixaPontuacao = Math.max(maxPontuacao - minPontuacao, 1);
    const MIN_BAR_HEIGHT = 140;
    const MAX_BAR_HEIGHT = 280;

    const calcularAlturaBarra = (pontuacaoTotal: number) => {
        if (pontosPodio.length === 1) {
            return MAX_BAR_HEIGHT;
        }
        const pesoNormalizado = (pontuacaoTotal - minPontuacao) / faixaPontuacao;
        const altura = MIN_BAR_HEIGHT + pesoNormalizado * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT);
        return Math.round(Math.max(MIN_BAR_HEIGHT, Math.min(MAX_BAR_HEIGHT, altura)));
    };
    
    const toggleDetalhes = (jogadorId: string) => {
        setMostrarDetalhes(prev => ({
            ...prev,
            [jogadorId]: !prev[jogadorId]
        }));
    };
    
    return (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4">
            <div className="bg-gradient-to-br from-yellow-50 to-amber-100 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border-4 border-yellow-400">
                {/* Cabeçalho */}
                <div className="bg-gradient-to-r from-yellow-400 to-amber-500 p-6 text-center border-b-4 border-yellow-600">
                    <h1 className="text-5xl font-bold text-white mb-2 drop-shadow-lg">
                        🏆 FIM DE JOGO 🏆
                    </h1>
                    
                    {empate ? (
                        <p className="text-2xl font-bold text-yellow-900">
                            🤝 EMPATE! 🤝
                        </p>
                    ) : (
                        <p className="text-2xl font-bold text-yellow-900">
                            🎉 Vencedor: {vencedor.jogadorNome} 🎉
                        </p>
                    )}
                    
                    <p className="text-lg text-yellow-800 mt-1">
                        {vencedor.pontuacaoTotal} pontos
                    </p>
                </div>
                
                {/* Pódio Visual */}
                <div className="p-6 bg-white bg-opacity-50 overflow-x-auto">
                    <div className="min-w-[320px] flex flex-wrap items-end justify-center gap-8 mb-6">
                        {podioJogadores.map((pontuacao, index) => {
                            const estilo = PODIO_STYLES[index] || estiloPadrao;
                            const altura = calcularAlturaBarra(pontuacao.pontuacaoTotal);
                            const largura = estilo.largura || 'w-24';

                            return (
                                <div
                                    key={pontuacao.jogadorId}
                                    className="flex flex-col items-center px-1"
                                >
                                    {/* Medalha */}
                                    <div className="text-4xl mb-2">
                                        {estilo.medalha}
                                    </div>
                                    
                                    {/* Pódio */}
                                    <div
                                        className={`
                                            ${largura}
                                            rounded-t-3xl flex flex-col justify-between items-center
                                            ${estilo.fundo}
                                            border-4
                                            ${estilo.borda}
                                            shadow-xl
                                            px-2 py-4 text-center text-white font-bold
                                        `}
                                        style={{ height: `${altura}px` }}
                                    >
                                        <div className="text-2xl">{index + 1}°</div>
                                        <div className="text-base font-semibold break-words">
                                            {pontuacao.jogadorNome}
                                        </div>
                                        <div className="text-3xl">{pontuacao.pontuacaoTotal}</div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
                
                {/* Pontuação Detalhada */}
                <div className="p-6 space-y-4">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">
                        📊 Pontuação Detalhada
                    </h2>
                    
                    {pontuacoesOrdenadas.map((pontuacao, index) => {
                        const cores = CORES_JOGADORES[pontuacao.jogadorCor] || CORES_JOGADORES.blue;
                        const detalhesVisiveis = mostrarDetalhes[pontuacao.jogadorId];
                        const ehVencedor = index === 0;
                        
                        return (
                            <div
                                key={pontuacao.jogadorId}
                                className={`
                                    rounded-lg border-2 overflow-hidden transition-all
                                    ${ehVencedor 
                                        ? 'bg-gradient-to-r from-yellow-100 to-amber-100 border-yellow-500 shadow-lg' 
                                        : `${cores.bg} ${cores.border}`
                                    }
                                `}
                            >
                                {/* Cabeçalho do Jogador */}
                                <div
                                    className="p-4 cursor-pointer hover:bg-opacity-80 transition-colors"
                                    onClick={() => toggleDetalhes(pontuacao.jogadorId)}
                                >
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-3">
                                            <span className="text-3xl font-bold text-gray-700">
                                                {index + 1}°
                                            </span>
                                            
                                            {ehVencedor && <span className="text-3xl">👑</span>}
                                            
                                            <div>
                                                <h3 className={`text-xl font-bold ${ehVencedor ? 'text-yellow-900' : cores.text}`}>
                                                    {pontuacao.jogadorNome}
                                                </h3>
                                                <p className="text-sm text-gray-600">
                                                    Clique para ver detalhes
                                                </p>
                                            </div>
                                        </div>
                                        
                                        <div className="flex items-center gap-3">
                                            <div className="text-right">
                                                <div className={`text-3xl font-bold ${ehVencedor ? 'text-yellow-800' : 'text-gray-800'}`}>
                                                    {pontuacao.pontuacaoTotal}
                                                </div>
                                                <div className="text-sm text-gray-600">pontos</div>
                                            </div>
                                            
                                            <span className={`text-2xl transition-transform ${detalhesVisiveis ? 'rotate-180' : ''}`}>
                                                ▼
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                
                                {/* Detalhes Expansíveis */}
                                {detalhesVisiveis && (
                                    <div className="px-4 pb-4 bg-white bg-opacity-60 space-y-3">
                                        {/* Pontos de Rotas */}
                                        <div className="flex justify-between items-center p-2 bg-blue-50 rounded">
                                            <span className="font-semibold text-blue-800">🛤️ Rotas Conquistadas</span>
                                            <span className="text-lg font-bold text-blue-900">+{pontuacao.pontosRotas}</span>
                                        </div>
                                        
                                        {/* Bilhetes Completos */}
                                        <div className="p-2 bg-green-50 rounded">
                                            <div className="flex justify-between items-center mb-2">
                                                <span className="font-semibold text-green-800">
                                                    ✅ Bilhetes Completos ({pontuacao.bilhetesCompletos.length})
                                                </span>
                                                <span className="text-lg font-bold text-green-900">
                                                    +{pontuacao.pontosBilhetesPositivos}
                                                </span>
                                            </div>
                                            {pontuacao.bilhetesCompletos.map((bilhete, i) => (
                                                <div key={i} className="text-sm text-green-700 ml-4">
                                                    • {bilhete.origem} ↔ {bilhete.destino} (+{bilhete.pontos})
                                                </div>
                                            ))}
                                        </div>
                                        
                                        {/* Bilhetes Incompletos */}
                                        {pontuacao.bilhetesIncompletos.length > 0 && (
                                            <div className="p-2 bg-red-50 rounded">
                                                <div className="flex justify-between items-center mb-2">
                                                    <span className="font-semibold text-red-800">
                                                        ❌ Bilhetes Incompletos ({pontuacao.bilhetesIncompletos.length})
                                                    </span>
                                                    <span className="text-lg font-bold text-red-900">
                                                        {pontuacao.pontosBilhetesNegativos}
                                                    </span>
                                                </div>
                                                {pontuacao.bilhetesIncompletos.map((bilhete, i) => (
                                                    <div key={i} className="text-sm text-red-700 ml-4">
                                                        • {bilhete.origem} ↔ {bilhete.destino} (-{bilhete.pontos})
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                        
                                        {/* Bônus Maior Caminho */}
                                        <div className={`
                                            flex justify-between items-center p-2 rounded
                                            ${pontuacao.bonusMaiorCaminho 
                                                ? 'bg-purple-100 border-2 border-purple-500' 
                                                : 'bg-gray-100'
                                            }
                                        `}>
                                            <div className="flex items-center gap-2">
                                                <span className={`font-semibold ${
                                                    pontuacao.bonusMaiorCaminho ? 'text-purple-800' : 'text-gray-600'
                                                }`}>
                                                    {pontuacao.bonusMaiorCaminho ? '🌟' : '➖'} Maior Caminho Contínuo
                                                </span>
                                                {pontuacao.tamanhoMaiorCaminho !== undefined && (
                                                    <span className="text-xs text-gray-600">
                                                        ({pontuacao.tamanhoMaiorCaminho} segmentos)
                                                    </span>
                                                )}
                                            </div>
                                            <span className={`text-lg font-bold ${
                                                pontuacao.bonusMaiorCaminho ? 'text-purple-900' : 'text-gray-500'
                                            }`}>
                                                {pontuacao.bonusMaiorCaminho ? '+10' : '0'}
                                            </span>
                                        </div>
                                        
                                        {/* Total */}
                                        <div className="flex justify-between items-center p-3 bg-gradient-to-r from-gray-200 to-gray-300 rounded-lg border-2 border-gray-400">
                                            <span className="text-lg font-bold text-gray-800">TOTAL</span>
                                            <span className="text-2xl font-bold text-gray-900">
                                                {pontuacao.pontuacaoTotal} pts
                                            </span>
                                        </div>
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
                
                {/* Botões de Ação */}
                <div className="p-6 bg-white bg-opacity-50 border-t-2 border-yellow-400 flex gap-3 justify-center">
                    {onJogarNovamente && (
                        <button
                            onClick={onJogarNovamente}
                            className="px-6 py-3 bg-green-500 text-white rounded-lg font-bold text-lg hover:bg-green-600 transition-colors shadow-lg"
                        >
                            🔄 Jogar Novamente
                        </button>
                    )}
                    
                    {onVoltarMenu && (
                        <button
                            onClick={onVoltarMenu}
                            className="px-6 py-3 bg-blue-500 text-white rounded-lg font-bold text-lg hover:bg-blue-600 transition-colors shadow-lg"
                        >
                            🏠 Voltar ao Menu
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
