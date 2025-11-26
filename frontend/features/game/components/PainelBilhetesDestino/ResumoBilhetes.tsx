/**
 * ResumoBilhetes - Resumo estatístico dos bilhetes
 * 
 * Responsabilidade única: Exibir estatísticas dos bilhetes
 */

'use client';

import type { BilhetesStats } from './types';

interface ResumoBilhetesProps {
  stats: BilhetesStats;
}

export function ResumoBilhetes({ stats }: ResumoBilhetesProps) {
  const {
    bilhetesCompletos,
    bilhetesIncompletos,
    pontosGanhos,
    pontosPerdidos,
    pontosTotaisPossiveis,
    balanco,
    percentualCompleto
  } = stats;

  return (
    <div className="bg-white rounded-lg p-4 shadow-inner">
      <h4 className="font-bold text-sm text-gray-700 mb-3">
        📊 Resumo
      </h4>
      
      <div className="grid grid-cols-2 gap-3">
        {/* Bilhetes Completos */}
        <div className="bg-green-50 rounded p-2 border-l-4 border-green-500">
          <div className="text-xs text-green-700">Completos</div>
          <div className="font-bold text-green-800">
            {bilhetesCompletos} bilhetes
          </div>
          <div className="text-sm text-green-600">
            +{pontosGanhos} pontos
          </div>
        </div>
        
        {/* Bilhetes Incompletos */}
        <div className="bg-red-50 rounded p-2 border-l-4 border-red-500">
          <div className="text-xs text-red-700">Incompletos</div>
          <div className="font-bold text-red-800">
            {bilhetesIncompletos} bilhetes
          </div>
          <div className="text-sm text-red-600">
            -{pontosPerdidos} pontos
          </div>
        </div>
      </div>
      
      <div className="mt-3 pt-3 border-t border-gray-200">
        {/* Balanço Total */}
        <div className="flex justify-between items-center">
          <span className="text-sm font-semibold text-gray-700">
            Balanço Total:
          </span>
          <span className={`text-lg font-bold ${
            balanco >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {balanco > 0 ? '+' : ''}{balanco} pts
          </span>
        </div>
        
        {/* Pontos Possíveis */}
        <div className="flex justify-between items-center mt-1">
          <span className="text-xs text-gray-500">
            Pontos possíveis:
          </span>
          <span className="text-sm text-gray-600">
            {pontosTotaisPossiveis} pts
          </span>
        </div>
        
        {/* Barra de progresso */}
        <div className="mt-2">
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-green-500 to-green-600 transition-all"
              style={{ width: `${percentualCompleto}%` }}
            />
          </div>
          <div className="text-xs text-center text-gray-500 mt-1">
            {percentualCompleto}% completo
          </div>
        </div>
      </div>
    </div>
  );
}
