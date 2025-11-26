/**
 * JogadorTrensCompactoItem - Versão compacta do item de jogador
 * 
 * GRASP - High Cohesion: Versão simplificada para modo compacto
 * 
 * Separado de JogadorTrensItem.tsx para seguir SRP
 */

import { CORES_JOGADORES } from '@/lib/constants/playerColors';
import type { JogadorTrensCompactoItemProps } from './types';

export function JogadorTrensCompactoItem({
    jogador,
    limiteAlerta,
    mudanca
}: JogadorTrensCompactoItemProps) {
    const emAlerta = jogador.trensRestantes <= limiteAlerta;
    const cores = CORES_JOGADORES[jogador.cor] || CORES_JOGADORES.blue;

    return (
        <div
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
}
