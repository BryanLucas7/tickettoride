/**
 * JogadorTrensItem - Item de jogador para modo expandido
 * 
 * GRASP - High Cohesion: Focado em exibir dados de trens de um jogador
 * 
 * Refatorado: JogadorTrensCompactoItem extraído para arquivo separado
 * seguindo o princípio de responsabilidade única (SRP)
 */

import { CORES_JOGADORES } from '@/lib/constants/playerColors';
import type { JogadorTrensItemProps } from './types';

export function JogadorTrensItem({
    jogador,
    trensIniciais,
    limiteAlerta,
    mostrarBarras,
    mudanca
}: JogadorTrensItemProps) {
    const porcentagem = (jogador.trensRestantes / trensIniciais) * 100;
    const cores = CORES_JOGADORES[jogador.cor] || CORES_JOGADORES.blue;
    const emAlerta = jogador.trensRestantes <= limiteAlerta;

    return (
        <div
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
}
