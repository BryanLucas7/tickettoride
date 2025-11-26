/**
 * Tipos para componentes de Mão de Cartas
 */

import { CorCarta, type CartaVagaoUI } from '@/types/game';

// Re-export para compatibilidade
export { CorCarta };
export type { CartaVagaoUI as CartaVagao };
export type { CartaVagaoUI };

/**
 * Props do Componente Principal
 */
export interface MaoCartasProps {
  cartas: CartaVagaoUI[];
  jogadorNome: string;
  isExpanded?: boolean;
  onCartaSelecionada?: (carta: CartaVagaoUI) => void;
  cartasSelecionadas?: CartaVagaoUI[];
  modoSelecao?: boolean;
}

/**
 * Cartas agrupadas por cor
 */
export interface CartasAgrupadas {
  [key: string]: CartaVagaoUI[];
}
