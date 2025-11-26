/**
 * CartaItem - Carta individual
 * 
 * Responsabilidade única: Renderizar uma carta de vagão
 */

'use client';

import { CorCarta, type CartaVagaoUI } from '@/types/game';
import { getCorConfig } from './constants/coresConfig';

interface CartaItemProps {
  carta: CartaVagaoUI;
  index: number;
  selecionada: boolean;
  modoSelecao: boolean;
  onClick: () => void;
}

export function CartaItem({
  carta,
  index,
  selecionada,
  modoSelecao,
  onClick
}: CartaItemProps) {
  const config = getCorConfig(carta.cor);
  
  return (
    <div
      onClick={onClick}
      className={`
        relative w-16 h-24 rounded-lg ${config.bg} border-4 ${config.border}
        flex flex-col items-center justify-center
        transition-all duration-200 transform
        ${modoSelecao ? 'cursor-pointer hover:scale-110 hover:shadow-lg' : ''}
        ${selecionada ? 'scale-110 ring-4 ring-yellow-400 shadow-xl' : ''}
      `}
    >
      {/* Ícone da Carta */}
      <span className="text-3xl mb-1">{config.emoji}</span>
      
      {/* Tipo da Carta */}
      <span className={`text-xs font-bold ${config.text} text-center px-1`}>
        {carta.cor === CorCarta.LOCOMOTIVA ? '🚂' : 'Vagão'}
      </span>
      
      {/* Indicador de Seleção */}
      {selecionada && (
        <div className="absolute -top-2 -right-2 bg-yellow-400 rounded-full w-6 h-6 flex items-center justify-center border-2 border-yellow-600">
          <span className="text-xs font-bold">✓</span>
        </div>
      )}
    </div>
  );
}
