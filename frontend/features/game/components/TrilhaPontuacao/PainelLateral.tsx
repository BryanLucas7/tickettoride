/**
 * Modo Painel Lateral para TrilhaPontuacao
 * 
 * GRASP - High Cohesion: Focado apenas em exibir placar em lista
 */

import type { PainelLateralProps, JogadorPlacar } from './types';
import { CORES_MARCADORES, extrairBgClasse } from './constants';
import { EstatisticasPlacar } from './EstatisticasPlacar';

/**
 * Item individual de jogador no painel lateral
 */
function JogadorPlacarItem({
    jogador,
    posicao,
    maxPontos,
    mudanca,
    mostrarNome
}: {
    jogador: JogadorPlacar;
    posicao: number;
    maxPontos: number;
    mudanca?: number;
    mostrarNome: boolean;
}) {
    const porcentagem = Math.min((jogador.pontos / maxPontos) * 100, 100);
    const corClasse = CORES_MARCADORES[jogador.cor] || CORES_MARCADORES.gray;

    return (
        <div className="bg-white rounded-lg p-3 shadow-md border-2 border-slate-200 transition-all hover:shadow-lg">
            <div className="flex items-center gap-3 mb-2">
                {/* Posição */}
                <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-slate-200 font-bold text-slate-700">
                    {posicao}°
                </div>

                {/* Marcador de cor */}
                <div className={`w-6 h-6 rounded-full border-2 ${corClasse}`} />

                {/* Nome */}
                {mostrarNome && (
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
                    className={`h-full transition-all duration-500 ${extrairBgClasse(corClasse)}`}
                    style={{ width: `${porcentagem}%` }}
                />
            </div>

            <div className="text-xs text-slate-500 mt-1 text-right">
                {porcentagem.toFixed(0)}% de {maxPontos}
            </div>
        </div>
    );
}

/**
 * Painel Lateral - Modo lista para exibir placar
 */
export function PainelLateral({
    jogadores,
    maxPontos,
    mudancas,
    mostrarNomes
}: PainelLateralProps) {
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
                {jogadoresOrdenados.map((jogador, index) => (
                    <JogadorPlacarItem
                        key={jogador.id}
                        jogador={jogador}
                        posicao={index + 1}
                        maxPontos={maxPontos}
                        mudanca={mudancas[jogador.id]}
                        mostrarNome={mostrarNomes}
                    />
                ))}
            </div>

            {/* Estatísticas */}
            <EstatisticasPlacar
                totalJogadores={jogadores.length}
                maxPontos={maxPontos}
            />
        </div>
    );
}
