/**
 * Tipos para componentes do Board (Mapa)
 */

import type { ReactNode } from 'react';
import type {
  CidadeComCoordenadas,
  MapaComCoordenadas,
  RotaApi,
} from '@/app/data/mapaBrasil';
import type { CorRotaString, CorJogador, RotaId, JogadorId } from '@/types/game';

// Re-exports
export type { CidadeComCoordenadas, MapaComCoordenadas, RotaApi };

/**
 * Interface para rota com informações do jogo
 */
export interface RotaDoJogo {
  id: RotaId;
  cidadeA: string;
  cidadeB: string;
  cor: CorRotaString;
  comprimento: number;
  proprietario_id: JogadorId | null;
  proprietario_nome: string | null;
  proprietario_cor: CorJogador | null;
  conquistada: boolean;
}

/**
 * Props do componente Board
 */
export interface BoardProps {
  mapa?: MapaComCoordenadas | null;
  rotasDoJogo?: RotaDoJogo[];
  rotaSelecionadaId?: string | null;
  onRotaSelecionada?: (rotaId: string | null) => void;
  renderRotaDetalhes?: (dados: {
    rotaMapa: RotaApi;
    rotaDoJogo?: RotaDoJogo;
  }) => ReactNode;
}

/**
 * Ponto no mapa
 */
export interface PontoMapa {
  x: number;
  y: number;
}
