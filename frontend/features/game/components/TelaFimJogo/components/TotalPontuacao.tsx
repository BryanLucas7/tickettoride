/**
 * TotalPontuacao - Resumo final da pontuação
 * 
 * Responsabilidade única: Exibir total de pontos
 */

'use client';

interface TotalPontuacaoProps {
  pontuacaoTotal: number;
}

export function TotalPontuacao({ pontuacaoTotal }: TotalPontuacaoProps) {
  return (
    <div className="flex justify-between items-center p-3 bg-gradient-to-r from-gray-200 to-gray-300 rounded-lg border-2 border-gray-400">
      <span className="text-lg font-bold text-gray-800">TOTAL</span>
      <span className="text-2xl font-bold text-gray-900">
        {pontuacaoTotal} pts
      </span>
    </div>
  );
}
