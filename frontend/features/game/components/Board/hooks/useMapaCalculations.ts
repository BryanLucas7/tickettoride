/**
 * useMapaCalculations - Hook para cálculos do mapa
 * 
 * Responsabilidade única: Gerenciar cálculos e lookups do mapa
 */

import { useCallback, useMemo } from 'react';
import type { CidadeComCoordenadas, MapaComCoordenadas, RotaApi, RotaDoJogo, PontoMapa } from '../types';

interface UseMapaCalculationsParams {
  mapa: MapaComCoordenadas | null | undefined;
  rotasDoJogo: RotaDoJogo[];
}

interface UseMapaCalculationsReturn {
  cidadeLookup: Map<string, CidadeComCoordenadas>;
  encontrarCidade: (id: string) => CidadeComCoordenadas | undefined;
  encontrarRotaDoJogo: (rotaId: string) => RotaDoJogo | undefined;
  calcularPontoMedio: (rota: RotaApi) => PontoMapa;
}

export function useMapaCalculations({
  mapa,
  rotasDoJogo
}: UseMapaCalculationsParams): UseMapaCalculationsReturn {
  // Lookup de cidades por ID
  const cidadeLookup = useMemo(() => {
    const lookup = new Map<string, CidadeComCoordenadas>();
    mapa?.cidades.forEach((cidade) => lookup.set(cidade.id, cidade));
    return lookup;
  }, [mapa]);

  // Encontrar cidade por ID
  const encontrarCidade = useCallback(
    (id: string): CidadeComCoordenadas | undefined => cidadeLookup.get(id),
    [cidadeLookup]
  );

  // Encontrar rota do jogo por ID
  const encontrarRotaDoJogo = useCallback(
    (rotaId: string): RotaDoJogo | undefined => 
      rotasDoJogo.find((r) => r.id === rotaId),
    [rotasDoJogo]
  );

  // Calcular ponto médio entre duas cidades
  const calcularPontoMedio = useCallback(
    (rota: RotaApi): PontoMapa => {
      const cidadeA = encontrarCidade(rota.cidadeA);
      const cidadeB = encontrarCidade(rota.cidadeB);
      if (!cidadeA || !cidadeB) return { x: 0, y: 0 };
      return {
        x: (cidadeA.x + cidadeB.x) / 2,
        y: (cidadeA.y + cidadeB.y) / 2,
      };
    },
    [encontrarCidade]
  );

  return {
    cidadeLookup,
    encontrarCidade,
    encontrarRotaDoJogo,
    calcularPontoMedio
  };
}
