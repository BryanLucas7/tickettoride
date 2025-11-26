/**
 * Marcador individual de jogador para a trilha circular
 */

import type { MarcadorJogadorProps } from './types';
import { CORES_MARCADORES, corParaFill } from './constants';

/**
 * Componente SVG para renderizar marcador de um jogador na trilha circular
 * 
 * GRASP - High Cohesion: Focado apenas em renderizar um marcador
 * Reutilizável em diferentes contextos SVG
 */
export function MarcadorJogador({ jogador, posicao, mudanca }: MarcadorJogadorProps) {
    const corClasse = CORES_MARCADORES[jogador.cor] || CORES_MARCADORES.gray;

    return (
        <g>
            {/* Marcador do jogador */}
            <circle
                cx={posicao.x}
                cy={posicao.y}
                r="12"
                className={corParaFill(corClasse)}
                stroke="#1e293b"
                strokeWidth="2"
            />

            {/* Nome e pontos */}
            <text
                x={posicao.x}
                y={posicao.y + 30}
                textAnchor="middle"
                className="text-sm font-bold fill-slate-800"
            >
                {jogador.nome}
            </text>

            <text
                x={posicao.x}
                y={posicao.y + 45}
                textAnchor="middle"
                className="text-xs font-semibold fill-slate-600"
            >
                {jogador.pontos} pts
            </text>

            {/* Indicador de mudança */}
            {mudanca !== undefined && mudanca !== 0 && (
                <text
                    x={posicao.x + 15}
                    y={posicao.y - 15}
                    textAnchor="start"
                    className={`text-xs font-bold ${mudanca > 0 ? 'fill-green-600' : 'fill-red-600'
                        }`}
                >
                    {mudanca > 0 ? '+' : ''}{mudanca}
                </text>
            )}
        </g>
    );
}
