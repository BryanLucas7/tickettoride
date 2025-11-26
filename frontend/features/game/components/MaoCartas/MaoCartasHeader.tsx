/**
 * MaoCartasHeader - Header expansível da mão de cartas
 * 
 * Responsabilidade única: Renderizar header com resumo e controle de expansão
 */

'use client';

import { CorCarta } from '@/types/game';
import { getCorConfig } from './constants/coresConfig';
import type { CartasAgrupadas } from './types';

interface MaoCartasHeaderProps {
  jogadorNome: string;
  totalCartas: number;
  isExpanded: boolean;
  onToggle: () => void;
  cartasAgrupadas: CartasAgrupadas;
  cores: string[];
}

export function MaoCartasHeader({
  jogadorNome,
  totalCartas,
  isExpanded,
  onToggle,
  cartasAgrupadas,
  cores
}: MaoCartasHeaderProps) {
  return (
    <div 
      className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 cursor-pointer hover:from-blue-700 hover:to-indigo-700 transition-colors"
      onClick={onToggle}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <span className="text-3xl">🎴</span>
          <div>
            <h3 className="text-white font-bold text-lg">
              Mão de {jogadorNome}
            </h3>
            <p className="text-blue-100 text-sm">
              {totalCartas} {totalCartas === 1 ? 'carta' : 'cartas'}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {/* Preview de cores quando colapsado */}
          {!isExpanded && (
            <div className="flex space-x-1">
              {cores.slice(0, 5).map(cor => {
                const config = getCorConfig(cor as CorCarta);
                return (
                  <div
                    key={cor}
                    className={`w-8 h-8 rounded-full ${config.bg} border-2 ${config.border} flex items-center justify-center text-xs font-bold ${config.text}`}
                  >
                    {cartasAgrupadas[cor].length}
                  </div>
                );
              })}
              {cores.length > 5 && (
                <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-xs font-bold">
                  +{cores.length - 5}
                </div>
              )}
            </div>
          )}
          
          {/* Botão de expansão */}
          <button 
            className="text-white text-2xl transition-transform duration-200" 
            style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
          >
            ▼
          </button>
        </div>
      </div>
    </div>
  );
}
