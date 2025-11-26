/**
 * GrupoCartas - Grupo de cartas de uma cor
 * 
 * Responsabilidade única: Renderizar grupo de cartas agrupadas por cor
 */

'use client';

import { CorCarta, type CartaVagaoUI } from '@/types/game';
import { getCorConfig } from './constants/coresConfig';
import { CartaItem } from './CartaItem';

interface GrupoCartasProps {
  cor: CorCarta;
  cartas: CartaVagaoUI[];
  cartasSelecionadas: CartaVagaoUI[];
  modoSelecao: boolean;
  onCartaClick: (carta: CartaVagaoUI) => void;
}

export function GrupoCartas({
  cor,
  cartas,
  cartasSelecionadas,
  modoSelecao,
  onCartaClick
}: GrupoCartasProps) {
  const config = getCorConfig(cor);
  
  const isCartaSelecionada = (carta: CartaVagaoUI): boolean => {
    return cartasSelecionadas.some(c => c.id === carta.id);
  };
  
  return (
    <div className="border-2 border-gray-200 rounded-lg p-3">
      {/* Header do Grupo */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">{config.emoji}</span>
          <span className="font-bold text-gray-800">
            {config.label}
          </span>
        </div>
        <span className="bg-gray-200 px-3 py-1 rounded-full text-sm font-semibold">
          {cartas.length} {cartas.length === 1 ? 'carta' : 'cartas'}
        </span>
      </div>
      
      {/* Cartas do Grupo */}
      <div className="flex flex-wrap gap-2">
        {cartas.map((carta, index) => (
          <CartaItem
            key={carta.id || `${cor}-${index}`}
            carta={carta}
            index={index}
            selecionada={isCartaSelecionada(carta)}
            modoSelecao={modoSelecao}
            onClick={() => onCartaClick(carta)}
          />
        ))}
      </div>
    </div>
  );
}
