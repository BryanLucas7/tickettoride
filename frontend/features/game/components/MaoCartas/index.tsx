/**
 * MaoCartas - Componente orquestrador refatorado
 * 
 * Princípios GRASP aplicados:
 * - SRP: Componentes extraídos com responsabilidade única
 * - Information Expert: Agrupamento memorizado
 * - High Cohesion: Cada componente focado em uma tarefa
 * 
 * Refatoração: 299 linhas → ~80 linhas (orquestrador)
 */

'use client';

import { useState, useMemo, useCallback } from 'react';
import { CorCarta, type CartaVagaoUI } from '@/types/game';
import { MaoCartasHeader } from './MaoCartasHeader';
import { GrupoCartas } from './GrupoCartas';
import { ResumoMao } from './ResumoMao';
import type { MaoCartasProps, CartasAgrupadas } from './types';

// Re-exports para compatibilidade
export { CorCarta };
export type { CartaVagaoUI as CartaVagao } from '@/types/game';
export type { MaoCartasProps };

export default function MaoCartas({
  cartas,
  jogadorNome,
  isExpanded: initialExpanded = false,
  onCartaSelecionada,
  cartasSelecionadas = [],
  modoSelecao = false
}: MaoCartasProps) {
  const [isExpanded, setIsExpanded] = useState(initialExpanded);
  
  // Memoriza agrupamento de cartas
  const cartasAgrupadas = useMemo((): CartasAgrupadas => {
    return cartas.reduce((grupos, carta) => {
      const cor = carta.cor;
      if (!grupos[cor]) {
        grupos[cor] = [];
      }
      grupos[cor].push(carta);
      return grupos;
    }, {} as CartasAgrupadas);
  }, [cartas]);
  
  const cores = useMemo(() => Object.keys(cartasAgrupadas).sort(), [cartasAgrupadas]);
  const totalCartas = cartas.length;
  
  const handleCartaClick = useCallback((carta: CartaVagaoUI) => {
    if (modoSelecao && onCartaSelecionada) {
      onCartaSelecionada(carta);
    }
  }, [modoSelecao, onCartaSelecionada]);
  
  return (
    <div className="bg-white rounded-lg shadow-lg border-2 border-gray-200 overflow-hidden">
      <MaoCartasHeader
        jogadorNome={jogadorNome}
        totalCartas={totalCartas}
        isExpanded={isExpanded}
        onToggle={() => setIsExpanded(!isExpanded)}
        cartasAgrupadas={cartasAgrupadas}
        cores={cores}
      />
      
      {/* Conteúdo Expandido */}
      {isExpanded && (
        <div className="p-4 space-y-3">
          {cores.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg">Nenhuma carta na mão</p>
              <p className="text-sm">Compre cartas para começar!</p>
            </div>
          ) : (
            cores.map(cor => (
              <GrupoCartas
                key={cor}
                cor={cor as CorCarta}
                cartas={cartasAgrupadas[cor]}
                cartasSelecionadas={cartasSelecionadas}
                modoSelecao={modoSelecao}
                onCartaClick={handleCartaClick}
              />
            ))
          )}
          
          <ResumoMao
            totalCartas={totalCartas}
            totalCores={cores.length}
            modoSelecao={modoSelecao}
            cartasSelecionadas={cartasSelecionadas.length}
          />
        </div>
      )}
    </div>
  );
}
