/**
 * Modo Compacto para ContadorTrens
 * 
 * GRASP - High Cohesion: Versão resumida para economizar espaço
 */

import type { ModoCompactoProps } from './types';
import { JogadorTrensCompactoItem } from './JogadorTrensCompactoItem';

/**
 * Modo Compacto - Versão resumida do contador de trens
 */
export function ModoCompacto({
    jogadores,
    limiteAlerta,
    mudancas
}: ModoCompactoProps) {
    return (
        <div className="bg-amber-100 rounded-lg border-2 border-amber-300 p-3">
            <div className="flex items-center gap-2 mb-2">
                <span className="text-xl">🚂</span>
                <span className="font-bold text-sm text-amber-900">Trens</span>
            </div>

            <div className="space-y-1">
                {jogadores.map(jogador => (
                    <JogadorTrensCompactoItem
                        key={jogador.id}
                        jogador={jogador}
                        limiteAlerta={limiteAlerta}
                        mudanca={mudancas[jogador.id]}
                    />
                ))}
            </div>
        </div>
    );
}
