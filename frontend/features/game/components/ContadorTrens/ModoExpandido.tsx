/**
 * Modo Expandido para ContadorTrens
 * 
 * GRASP - High Cohesion: Focado em exibir detalhes completos dos trens
 */

import type { ModoExpandidoProps } from './types';
import { JogadorTrensItem } from './JogadorTrensItem';
import { AlertaFimJogo } from './AlertaFimJogo';

/**
 * Resumo de estatísticas do contador
 */
function ResumoTrens({
    jogadores,
    trensIniciais
}: {
    jogadores: { nome: string; trensRestantes: number }[];
    trensIniciais: number;
}) {
    const jogadorComMenosTrens = [...jogadores].sort(
        (a, b) => a.trensRestantes - b.trensRestantes
    )[0];

    return (
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
    );
}

/**
 * Modo Expandido - Versão detalhada do contador de trens
 */
export function ModoExpandido({
    jogadores,
    trensIniciais,
    limiteAlerta,
    mostrarBarras,
    mudancas,
    alertaFimJogo
}: ModoExpandidoProps) {
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

                <AlertaFimJogo visivel={alertaFimJogo} />
            </div>

            {/* Lista de jogadores */}
            <div className="space-y-3">
                {jogadores.map(jogador => (
                    <JogadorTrensItem
                        key={jogador.id}
                        jogador={jogador}
                        trensIniciais={trensIniciais}
                        limiteAlerta={limiteAlerta}
                        mostrarBarras={mostrarBarras}
                        mudanca={mudancas[jogador.id]}
                    />
                ))}
            </div>

            {/* Resumo */}
            <ResumoTrens jogadores={jogadores} trensIniciais={trensIniciais} />
        </div>
    );
}
