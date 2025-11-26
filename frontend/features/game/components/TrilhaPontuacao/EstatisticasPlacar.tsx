/**
 * Estatísticas resumidas do placar
 */

interface EstatisticasPlacarProps {
    totalJogadores: number;
    maxPontos: number;
}

/**
 * Componente para exibir estatísticas do placar
 * 
 * GRASP - High Cohesion: Focado apenas em exibir estatísticas
 */
export function EstatisticasPlacar({ totalJogadores, maxPontos }: EstatisticasPlacarProps) {
    return (
        <div className="mt-4 pt-3 border-t-2 border-slate-200">
            <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="bg-slate-50 rounded p-2">
                    <div className="text-xs text-slate-600">Total de Jogadores</div>
                    <div className="font-bold text-slate-800">{totalJogadores}</div>
                </div>

                <div className="bg-slate-50 rounded p-2">
                    <div className="text-xs text-slate-600">Pontos Máximos</div>
                    <div className="font-bold text-slate-800">{maxPontos}</div>
                </div>
            </div>
        </div>
    );
}
