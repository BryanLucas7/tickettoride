/**
 * BilheteCard - Card individual de bilhete
 * 
 * Responsabilidade única: Exibir um bilhete de destino
 */

'use client';

import type { BilheteDestinoUI } from './types';

interface BilheteCardProps {
  bilhete: BilheteDestinoUI;
  mostrarStatus?: boolean;
}

export function BilheteCard({ bilhete, mostrarStatus = true }: BilheteCardProps) {
  const { origem, destino, pontos, completo } = bilhete;
  
  return (
    <div className={`
      rounded-lg p-3 border-2 transition-all
      ${completo 
        ? 'bg-green-50 border-green-400 shadow-sm' 
        : 'bg-white border-purple-300 shadow-md'
      }
    `}>
      <div className="flex items-center justify-between">
        {/* Origem e Destino */}
        <div className="flex items-center gap-2 flex-1">
          <span className="font-bold text-purple-900 text-sm">
            {origem}
          </span>
          <span className="text-2xl">
            {completo ? '✅' : '➡️'}
          </span>
          <span className="font-bold text-purple-900 text-sm">
            {destino}
          </span>
        </div>
        
        {/* Pontos */}
        <div className={`
          px-3 py-1 rounded-full font-bold text-sm
          ${completo 
            ? 'bg-green-200 text-green-800' 
            : 'bg-purple-200 text-purple-800'
          }
        `}>
          {completo ? '+' : ''}{pontos} pts
        </div>
      </div>
      
      {/* Status visual */}
      {mostrarStatus && (
        <div className="mt-2 text-xs flex items-center gap-2">
          {completo ? (
            <>
              <span className="text-green-600">●</span>
              <span className="text-green-700 font-semibold">
                Bilhete completo - Pontos garantidos!
              </span>
            </>
          ) : (
            <>
              <span className="text-orange-500">●</span>
              <span className="text-orange-700">
                Conecte {origem} ↔ {destino} para ganhar {pontos} pontos
              </span>
            </>
          )}
        </div>
      )}
    </div>
  );
}
