/**
 * TelaFimJogo - Componente orquestrador refatorado
 * 
 * Princípios GRASP aplicados:
 * - SRP: Componentes extraídos com responsabilidade única
 * - Low Coupling: Subcomponentes independentes
 * - High Cohesion: Cada componente focado em uma tarefa
 * 
 * Refatoração: 366 linhas → ~80 linhas (orquestrador)
 */

'use client';

import { useState, useMemo } from 'react';
import { CabecalhoVitoria } from './CabecalhoVitoria';
import { PodioVisual } from './PodioVisual';
import { PontuacaoDetalhadaCard } from './PontuacaoDetalhadaCard';
import { BotoesNavegacao } from './BotoesNavegacao';
import type { TelaFimJogoProps } from './types';

// Re-exportar tipos para uso externo
export type { PontuacaoFinal, BilheteResultado, TelaFimJogoProps } from './types';

export default function TelaFimJogo({
  pontuacoes,
  exibir,
  onJogarNovamente,
  onVoltarMenu
}: TelaFimJogoProps) {
  const [mostrarDetalhes, setMostrarDetalhes] = useState<Record<string, boolean>>({});
  
  // Memoiza ordenação para evitar recálculos desnecessários
  const pontuacoesOrdenadas = useMemo(() => 
    [...pontuacoes].sort((a, b) => b.pontuacaoTotal - a.pontuacaoTotal),
    [pontuacoes]
  );
  
  if (!exibir) return null;
  
  const vencedor = pontuacoesOrdenadas[0];
  const empate = pontuacoesOrdenadas.filter(
    p => p.pontuacaoTotal === vencedor.pontuacaoTotal
  ).length > 1;
  
  const toggleDetalhes = (jogadorId: string) => {
    setMostrarDetalhes(prev => ({
      ...prev,
      [jogadorId]: !prev[jogadorId]
    }));
  };
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4">
      <div className="bg-gradient-to-br from-yellow-50 to-amber-100 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto border-4 border-yellow-400">
        
        <CabecalhoVitoria
          vencedorNome={vencedor.jogadorNome}
          vencedorPontuacao={vencedor.pontuacaoTotal}
          empate={empate}
        />
        
        <PodioVisual pontuacoes={pontuacoesOrdenadas} />
        
        {/* Pontuação Detalhada */}
        <div className="p-6 space-y-4">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            📊 Pontuação Detalhada
          </h2>
          
          {pontuacoesOrdenadas.map((pontuacao, index) => (
            <PontuacaoDetalhadaCard
              key={pontuacao.jogadorId}
              pontuacao={pontuacao}
              posicao={index + 1}
              ehVencedor={index === 0}
              expandido={mostrarDetalhes[pontuacao.jogadorId] || false}
              onToggleExpansao={() => toggleDetalhes(pontuacao.jogadorId)}
            />
          ))}
        </div>
        
        <BotoesNavegacao
          onJogarNovamente={onJogarNovamente}
          onVoltarMenu={onVoltarMenu}
        />
      </div>
    </div>
  );
}
