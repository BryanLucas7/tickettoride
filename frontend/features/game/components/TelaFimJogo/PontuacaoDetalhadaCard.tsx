/**
 * PontuacaoDetalhadaCard - Card expandível com detalhes da pontuação
 * 
 * Refatorado seguindo SRP: cada seção é um componente independente
 * - CabecalhoPontuacao: posição, nome e total
 * - DetalheRotas: pontos de rotas conquistadas
 * - DetalheBilhetes: bilhetes completos e incompletos
 * - BonusMaiorCaminho: bônus do maior caminho
 * - TotalPontuacao: resumo final
 * 
 * Redução: 160 linhas → ~70 linhas
 */

'use client';

import { CORES_JOGADORES } from '@/lib/constants/playerColors';
import type { PontuacaoFinal } from './types';
import {
  CabecalhoPontuacao,
  DetalheRotas,
  DetalheBilhetes,
  BonusMaiorCaminho,
  TotalPontuacao
} from './components';

interface PontuacaoDetalhadaCardProps {
  pontuacao: PontuacaoFinal;
  posicao: number;
  ehVencedor: boolean;
  expandido: boolean;
  onToggleExpansao: () => void;
}

export function PontuacaoDetalhadaCard({
  pontuacao,
  posicao,
  ehVencedor,
  expandido,
  onToggleExpansao
}: PontuacaoDetalhadaCardProps) {
  const cores = CORES_JOGADORES[pontuacao.jogadorCor] || CORES_JOGADORES.blue;

  return (
    <div
      className={`
        rounded-lg border-2 overflow-hidden transition-all
        ${ehVencedor 
          ? 'bg-gradient-to-r from-yellow-100 to-amber-100 border-yellow-500 shadow-lg' 
          : `${cores.bg} ${cores.border}`
        }
      `}
    >
      <CabecalhoPontuacao
        posicao={posicao}
        nome={pontuacao.jogadorNome}
        pontuacaoTotal={pontuacao.pontuacaoTotal}
        ehVencedor={ehVencedor}
        expandido={expandido}
        coresText={cores.text}
        onClick={onToggleExpansao}
      />
      
      {expandido && (
        <div className="px-4 pb-4 bg-white bg-opacity-60 space-y-3">
          <DetalheRotas pontosRotas={pontuacao.pontosRotas} />
          
          <DetalheBilhetes
            bilhetesCompletos={pontuacao.bilhetesCompletos}
            bilhetesIncompletos={pontuacao.bilhetesIncompletos}
            pontosBilhetesPositivos={pontuacao.pontosBilhetesPositivos}
            pontosBilhetesNegativos={pontuacao.pontosBilhetesNegativos}
          />
          
          <BonusMaiorCaminho
            bonus={pontuacao.bonusMaiorCaminho}
            tamanho={pontuacao.tamanhoMaiorCaminho}
          />
          
          <TotalPontuacao pontuacaoTotal={pontuacao.pontuacaoTotal} />
        </div>
      )}
    </div>
  );
}
