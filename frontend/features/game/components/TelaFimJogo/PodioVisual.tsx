/**
 * PodioVisual - Visualização do pódio com barras proporcionais
 * 
 * Responsabilidade única: Renderizar o pódio visual dos jogadores
 */

'use client';

import type { PontuacaoFinal } from './types';
import { calcularAlturaBarra, getEstiloPodio } from './utils/calcularAlturaBarra';

interface PodioVisualProps {
  pontuacoes: PontuacaoFinal[];
  maxJogadores?: number;
}

export function PodioVisual({ pontuacoes, maxJogadores = 5 }: PodioVisualProps) {
  const podioJogadores = pontuacoes.slice(0, Math.min(maxJogadores, pontuacoes.length));
  const pontosPodio = podioJogadores.map((p) => p.pontuacaoTotal);
  const maxPontuacao = pontosPodio.length ? Math.max(...pontosPodio) : 0;
  const minPontuacao = pontosPodio.length ? Math.min(...pontosPodio) : 0;

  return (
    <div className="p-6 bg-white bg-opacity-50 overflow-x-auto">
      <div className="min-w-[320px] flex flex-wrap items-end justify-center gap-8 mb-6">
        {podioJogadores.map((pontuacao, index) => {
          const estilo = getEstiloPodio(index);
          const altura = calcularAlturaBarra({
            pontuacaoTotal: pontuacao.pontuacaoTotal,
            minPontuacao,
            maxPontuacao,
            totalJogadores: podioJogadores.length
          });
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
              
              {/* Barra do Pódio */}
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
  );
}
