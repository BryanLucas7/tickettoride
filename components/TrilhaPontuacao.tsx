/**
 * TRILHA DE PONTUAÇÃO VISUAL - Componente UI
 * ===========================================
 * 
 * Exibe a pontuação de cada jogador em tempo real com marcadores coloridos.
 * Pode ser renderizada como trilha circular ao redor do mapa ou painel lateral.
 * 
 * Princípios GRASP aplicados:
 * - Information Expert: Placar calcula e gerencia pontos dos jogadores
 * - Low Coupling: UI apenas observa mudanças no placar
 * - High Cohesion: Componente focado apenas em exibir pontuação
 * 
 * Padrão GoF: Observer Pattern - Observa mudanças no placar e atualiza UI
 */

'use client';

import { useState, useEffect } from 'react';

/**
 * Interface de Jogador para exibição no placar
 */
export interface JogadorPlacar {
    id: string;
    nome: string;
    pontos: number;
    cor: string; // Cor do marcador (ex: 'red', 'blue', 'green', 'yellow', 'purple')
}

/**
 * Props do Componente
 */
interface TrilhaPontuacaoProps {
    jogadores: JogadorPlacar[];
    maxPontos?: number;        // Pontos máximos da trilha (padrão: 100)
    modo?: 'trilha' | 'painel'; // Modo de visualização
    largura?: number;           // Largura em pixels (modo trilha)
    altura?: number;            // Altura em pixels (modo trilha)
    animarMudancas?: boolean;   // Anima mudanças de pontuação
    mostrarNomes?: boolean;     // Mostra nomes dos jogadores
}

/**
 * Mapa de cores CSS para marcadores
 */
const CORES_MARCADORES: Record<string, string> = {
    red: 'bg-red-500 border-red-700',
    blue: 'bg-blue-500 border-blue-700',
    green: 'bg-green-500 border-green-700',
    yellow: 'bg-yellow-400 border-yellow-600',
    purple: 'bg-purple-500 border-purple-700',
    orange: 'bg-orange-500 border-orange-700',
    pink: 'bg-pink-500 border-pink-700',
    teal: 'bg-teal-500 border-teal-700',
    indigo: 'bg-indigo-500 border-indigo-700',
    gray: 'bg-gray-500 border-gray-700',
};

/**
 * Componente Principal
 * 
 * GRASP - Information Expert:
 * Recebe dados do placar e apresenta pontuação de forma visual
 * 
 * GRASP - Low Coupling:
 * Não conhece lógica de cálculo de pontos, apenas apresenta
 * 
 * Observer Pattern:
 * Reage a mudanças no array de jogadores (pontos)
 */
export default function TrilhaPontuacao({
    jogadores,
    maxPontos = 100,
    modo = 'painel',
    largura = 600,
    altura = 600,
    animarMudancas = true,
    mostrarNomes = true
}: TrilhaPontuacaoProps) {
    const [jogadoresAnteriores, setJogadoresAnteriores] = useState(jogadores);
    const [mudancas, setMudancas] = useState<Record<string, number>>({});
    
    /**
     * Observer Pattern:
     * Detecta mudanças na pontuação e registra para animação
     */
    useEffect(() => {
        if (!animarMudancas) return;
        
        const novasMudancas: Record<string, number> = {};
        
        jogadores.forEach(jogador => {
            const anterior = jogadoresAnteriores.find(j => j.id === jogador.id);
            if (anterior && anterior.pontos !== jogador.pontos) {
                novasMudancas[jogador.id] = jogador.pontos - anterior.pontos;
            }
        });
        
        if (Object.keys(novasMudancas).length > 0) {
            setMudancas(novasMudancas);
            
            // Remove indicadores de mudança após 2 segundos
            setTimeout(() => {
                setMudancas({});
            }, 2000);
        }
        
        setJogadoresAnteriores(jogadores);
    }, [jogadores, animarMudancas, jogadoresAnteriores]);
    
    // Renderiza modo apropriado
    if (modo === 'trilha') {
        return (
            <TrilhaCircular
                jogadores={jogadores}
                maxPontos={maxPontos}
                largura={largura}
                altura={altura}
                mudancas={mudancas}
            />
        );
    }
    
    return (
        <PainelLateral
            jogadores={jogadores}
            maxPontos={maxPontos}
            mudancas={mudancas}
            mostrarNomes={mostrarNomes}
        />
    );
}

/**
 * Modo Painel Lateral
 * 
 * GRASP - High Cohesion: Focado apenas em exibir placar em lista
 */
function PainelLateral({
    jogadores,
    maxPontos,
    mudancas,
    mostrarNomes
}: {
    jogadores: JogadorPlacar[];
    maxPontos: number;
    mudancas: Record<string, number>;
    mostrarNomes: boolean;
}) {
    // Ordena jogadores por pontuação (maior para menor)
    const jogadoresOrdenados = [...jogadores].sort((a, b) => b.pontos - a.pontos);
    
    const lider = jogadoresOrdenados[0];
    
    return (
        <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg shadow-lg border-2 border-slate-300 p-4">
            {/* Cabeçalho */}
            <div className="flex items-center gap-2 mb-4 pb-3 border-b-2 border-slate-300">
                <span className="text-3xl">🏆</span>
                <div>
                    <h3 className="font-bold text-lg text-slate-900">Placar</h3>
                    <p className="text-sm text-slate-600">
                        Líder: <span className="font-semibold">{lider?.nome || '—'}</span>
                    </p>
                </div>
            </div>
            
            {/* Lista de jogadores */}
            <div className="space-y-3">
                {jogadoresOrdenados.map((jogador, index) => {
                    const mudanca = mudancas[jogador.id];
                    const porcentagem = Math.min((jogador.pontos / maxPontos) * 100, 100);
                    const corClasse = CORES_MARCADORES[jogador.cor] || CORES_MARCADORES.gray;
                    
                    return (
                        <div
                            key={jogador.id}
                            className="bg-white rounded-lg p-3 shadow-md border-2 border-slate-200 transition-all hover:shadow-lg"
                        >
                            <div className="flex items-center gap-3 mb-2">
                                {/* Posição */}
                                <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-slate-200 font-bold text-slate-700">
                                    {index + 1}°
                                </div>
                                
                                {/* Marcador de cor */}
                                <div className={`w-6 h-6 rounded-full border-2 ${corClasse}`} />
                                
                                {/* Nome */}
                                {mostrarNomes && (
                                    <span className="font-bold text-slate-900 flex-1">
                                        {jogador.nome}
                                    </span>
                                )}
                                
                                {/* Pontos */}
                                <div className="flex items-center gap-2">
                                    <span className="text-2xl font-bold text-slate-800">
                                        {jogador.pontos}
                                    </span>
                                    <span className="text-sm text-slate-500">pts</span>
                                    
                                    {/* Indicador de mudança */}
                                    {mudanca !== undefined && mudanca !== 0 && (
                                        <span className={`
                                            text-xs font-bold px-2 py-1 rounded-full
                                            ${mudanca > 0 
                                                ? 'bg-green-100 text-green-700' 
                                                : 'bg-red-100 text-red-700'
                                            }
                                            animate-bounce
                                        `}>
                                            {mudanca > 0 ? '+' : ''}{mudanca}
                                        </span>
                                    )}
                                </div>
                            </div>
                            
                            {/* Barra de progresso */}
                            <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                                <div
                                    className={`h-full transition-all duration-500 ${
                                        corClasse.split(' ')[0]
                                    }`}
                                    style={{ width: `${porcentagem}%` }}
                                />
                            </div>
                            
                            <div className="text-xs text-slate-500 mt-1 text-right">
                                {porcentagem.toFixed(0)}% de {maxPontos}
                            </div>
                        </div>
                    );
                })}
            </div>
            
            {/* Estatísticas */}
            <div className="mt-4 pt-3 border-t-2 border-slate-200">
                <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="bg-slate-50 rounded p-2">
                        <div className="text-xs text-slate-600">Total de Jogadores</div>
                        <div className="font-bold text-slate-800">{jogadores.length}</div>
                    </div>
                    
                    <div className="bg-slate-50 rounded p-2">
                        <div className="text-xs text-slate-600">Pontos Máximos</div>
                        <div className="font-bold text-slate-800">{maxPontos}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

/**
 * Modo Trilha Circular
 * 
 * GRASP - High Cohesion: Focado apenas em exibir placar em trilha circular
 */
function TrilhaCircular({
    jogadores,
    maxPontos,
    largura,
    altura,
    mudancas
}: {
    jogadores: JogadorPlacar[];
    maxPontos: number;
    largura: number;
    altura: number;
    mudancas: Record<string, number>;
}) {
    // Calcula centro e raio
    const centroX = largura / 2;
    const centroY = altura / 2;
    const raio = Math.min(largura, altura) / 2 - 40;
    
    /**
     * Calcula posição X,Y na trilha circular baseado nos pontos
     */
    const calcularPosicao = (pontos: number) => {
        // Trilha começa no topo (270°) e vai no sentido horário
        const angulo = 270 + (pontos / maxPontos) * 360;
        const radianos = (angulo * Math.PI) / 180;
        
        return {
            x: centroX + raio * Math.cos(radianos),
            y: centroY + raio * Math.sin(radianos)
        };
    };
    
    return (
        <div className="relative bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg shadow-lg border-2 border-slate-300 p-4">
            <svg width={largura} height={altura} className="mx-auto">
                {/* Trilha de fundo */}
                <circle
                    cx={centroX}
                    cy={centroY}
                    r={raio}
                    fill="none"
                    stroke="#cbd5e1"
                    strokeWidth="8"
                />
                
                {/* Marcações de pontos (0, 25, 50, 75, 100) */}
                {[0, 25, 50, 75, 100].map(pontos => {
                    if (pontos > maxPontos) return null;
                    
                    const pos = calcularPosicao(pontos);
                    
                    return (
                        <g key={pontos}>
                            {/* Marca na trilha */}
                            <circle
                                cx={pos.x}
                                cy={pos.y}
                                r="4"
                                fill="#64748b"
                            />
                            
                            {/* Texto de pontuação */}
                            <text
                                x={pos.x}
                                y={pos.y - 15}
                                textAnchor="middle"
                                className="text-xs font-semibold fill-slate-600"
                            >
                                {pontos}
                            </text>
                        </g>
                    );
                })}
                
                {/* Marcadores dos jogadores */}
                {jogadores.map(jogador => {
                    const pos = calcularPosicao(Math.min(jogador.pontos, maxPontos));
                    const corClasse = CORES_MARCADORES[jogador.cor] || CORES_MARCADORES.gray;
                    const mudanca = mudancas[jogador.id];
                    
                    return (
                        <g key={jogador.id}>
                            {/* Marcador do jogador */}
                            <circle
                                cx={pos.x}
                                cy={pos.y}
                                r="12"
                                className={corClasse.split(' ')[0].replace('bg-', 'fill-')}
                                stroke="#1e293b"
                                strokeWidth="2"
                            />
                            
                            {/* Nome e pontos */}
                            <text
                                x={pos.x}
                                y={pos.y + 30}
                                textAnchor="middle"
                                className="text-sm font-bold fill-slate-800"
                            >
                                {jogador.nome}
                            </text>
                            
                            <text
                                x={pos.x}
                                y={pos.y + 45}
                                textAnchor="middle"
                                className="text-xs font-semibold fill-slate-600"
                            >
                                {jogador.pontos} pts
                            </text>
                            
                            {/* Indicador de mudança */}
                            {mudanca !== undefined && mudanca !== 0 && (
                                <text
                                    x={pos.x + 15}
                                    y={pos.y - 15}
                                    textAnchor="start"
                                    className={`text-xs font-bold ${
                                        mudanca > 0 ? 'fill-green-600' : 'fill-red-600'
                                    }`}
                                >
                                    {mudanca > 0 ? '+' : ''}{mudanca}
                                </text>
                            )}
                        </g>
                    );
                })}
                
                {/* Texto central */}
                <text
                    x={centroX}
                    y={centroY - 10}
                    textAnchor="middle"
                    className="text-3xl font-bold fill-slate-800"
                >
                    🏆
                </text>
                
                <text
                    x={centroX}
                    y={centroY + 15}
                    textAnchor="middle"
                    className="text-lg font-bold fill-slate-700"
                >
                    Placar
                </text>
            </svg>
        </div>
    );
}
