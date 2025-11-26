/**
 * BilheteSelecaoCard - Card de bilhete para seleção
 * 
 * Responsabilidade única: Renderizar um bilhete selecionável
 */

'use client';

import type { BilheteDestino } from '../hooks/useBilhetesFlow';

interface BilheteSelecaoCardProps {
  bilhete: BilheteDestino;
  selecionado: boolean;
  onToggle: () => void;
}

export function BilheteSelecaoCard({ 
  bilhete, 
  selecionado, 
  onToggle 
}: BilheteSelecaoCardProps) {
  return (
    <div
      onClick={onToggle}
      className={`
        p-6 rounded-lg border-2 cursor-pointer transition-all
        ${selecionado 
          ? 'border-blue-600 bg-blue-50 shadow-lg' 
          : 'border-gray-300 bg-white hover:border-blue-400 hover:shadow-md'
        }
      `}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-2xl">🎫</span>
            <h3 className="text-xl font-semibold text-gray-800">
              {bilhete.cidadeOrigem} → {bilhete.cidadeDestino}
            </h3>
          </div>
          <p className="text-gray-600 ml-10">
            Complete esta rota para ganhar pontos
          </p>
        </div>
        <div className="text-center ml-4">
          <div className="bg-yellow-400 text-gray-900 font-bold text-2xl rounded-full w-16 h-16 flex items-center justify-center">
            {bilhete.pontos}
          </div>
          <p className="text-xs text-gray-600 mt-1">pontos</p>
        </div>
      </div>
      {selecionado && (
        <div className="mt-3 flex items-center gap-2 text-blue-600 font-medium">
          <span className="text-xl">✓</span>
          Selecionado
        </div>
      )}
    </div>
  );
}
