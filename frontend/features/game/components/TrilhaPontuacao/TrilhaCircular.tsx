/**
 * Modo Trilha Circular para TrilhaPontuacao
 * 
 * GRASP - High Cohesion: Focado apenas em exibir placar em trilha circular
 */

import type { TrilhaCircularProps } from './types';
import { calcularPosicaoCircular } from './utils/calcularPosicaoCircular';
import { MarcadorJogador } from './MarcadorJogador';

/**
 * Marcações de pontuação na trilha
 */
function MarcacoesPontuacao({
    maxPontos,
    centroX,
    centroY,
    raio
}: {
    maxPontos: number;
    centroX: number;
    centroY: number;
    raio: number;
}) {
    const pontuacoesMarcadas = [0, 25, 50, 75, 100].filter(p => p <= maxPontos);

    return (
        <>
            {pontuacoesMarcadas.map(pontos => {
                const pos = calcularPosicaoCircular(pontos, maxPontos, centroX, centroY, raio);

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
        </>
    );
}

/**
 * Texto central da trilha
 */
function TextoCentral({ centroX, centroY }: { centroX: number; centroY: number }) {
    return (
        <>
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
        </>
    );
}

/**
 * Trilha Circular - Modo SVG circular para exibir placar
 */
export function TrilhaCircular({
    jogadores,
    maxPontos,
    largura,
    altura,
    mudancas
}: TrilhaCircularProps) {
    // Calcula centro e raio
    const centroX = largura / 2;
    const centroY = altura / 2;
    const raio = Math.min(largura, altura) / 2 - 40;

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
                <MarcacoesPontuacao
                    maxPontos={maxPontos}
                    centroX={centroX}
                    centroY={centroY}
                    raio={raio}
                />

                {/* Marcadores dos jogadores */}
                {jogadores.map(jogador => {
                    const pos = calcularPosicaoCircular(
                        Math.min(jogador.pontos, maxPontos),
                        maxPontos,
                        centroX,
                        centroY,
                        raio
                    );

                    return (
                        <MarcadorJogador
                            key={jogador.id}
                            jogador={jogador}
                            posicao={pos}
                            mudanca={mudancas[jogador.id]}
                        />
                    );
                })}

                {/* Texto central */}
                <TextoCentral centroX={centroX} centroY={centroY} />
            </svg>
        </div>
    );
}
