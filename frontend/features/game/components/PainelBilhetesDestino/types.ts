/**
 * Tipos para componentes de Painel de Bilhetes
 */

import { type BilheteDestinoUI } from '@/types/game';

export type { BilheteDestinoUI };

/**
 * Props do Componente Principal
 */
export interface PainelBilhetesDestinoProps {
  bilhetes: BilheteDestinoUI[];
  jogadorNome: string;
  modoSecreto?: boolean;
  isExpanded?: boolean;
  mostrarStatus?: boolean;
}

/**
 * Estatísticas calculadas dos bilhetes
 */
export interface BilhetesStats {
  totalBilhetes: number;
  bilhetesCompletos: number;
  bilhetesIncompletos: number;
  pontosGanhos: number;
  pontosPerdidos: number;
  pontosTotaisPossiveis: number;
  balanco: number;
  percentualCompleto: number;
}
