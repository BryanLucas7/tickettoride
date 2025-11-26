/**
 * Dados visuais do mapa (apenas coordenadas e cores).
 * A topologia (cidades/rotas) vem do backend via /map/config.
 */

import type { CorRotaString } from '@/types/game'

export interface CidadeApi {
  id: string;
  nome: string;
}

export interface RotaApi {
  id: string;
  cidadeA: string;
  cidadeB: string;
  cor: string;
  comprimento: number;
}

export interface MapaApiResponse {
  map_id?: string;
  cidades: CidadeApi[];
  rotas: RotaApi[];
}

export interface CidadeComCoordenadas extends CidadeApi {
  x: number;
  y: number;
}

export interface MapaComCoordenadas {
  cidades: CidadeComCoordenadas[];
  rotas: RotaApi[];
}

const CIDADE_COORDENADAS: Record<string, { x: number; y: number }> = {
  PORTO_ALEGRE: { x: 430, y: 580 },
  BAURU: { x: 465, y: 455 },
  RIO_DE_JANEIRO: { x: 565, y: 465 },
  BRASILIA: { x: 480, y: 370 },
  CAMPO_GRANDE: { x: 385, y: 435 },
  CUIABA: { x: 350, y: 340 },
  SALVADOR: { x: 605, y: 320 },
  RECIFE: { x: 670, y: 240 },
  FORTALEZA: { x: 620, y: 190 },
  BELEM: { x: 480, y: 140 },
  MANAUS: { x: 300, y: 160 },
  RIO_BRANCO: { x: 190, y: 280 },
  PALMAS: { x: 470, y: 280 },
};

export const CORES_HEX: Record<CorRotaString | 'locomotiva', string> = {
  vermelho: "#DC2626",
  azul: "#2563EB",
  verde: "#16A34A",
  amarelo: "#FBBF24",
  preto: "#1F2937",
  laranja: "#EA580C",
  roxo: "#8B5CF6",
  branco: "#ffffff",
  cinza: "#b7b7b7",
  locomotiva: "#6B7280",
};

type CorHex = CorRotaString | 'locomotiva';

function isCorHex(cor: string): cor is CorHex {
  return cor in CORES_HEX;
}

export function obterCorHex(cor?: string | null): string {
  if (!cor) return CORES_HEX.cinza;
  const normalizada = cor.toLowerCase();
  return isCorHex(normalizada) ? CORES_HEX[normalizada] : CORES_HEX.cinza;
}

export function anexarCoordenadasMapa(apiMapa: MapaApiResponse): MapaComCoordenadas {
  const cidades = (apiMapa.cidades || [])
    .map((cidade) => {
      const coords = CIDADE_COORDENADAS[cidade.id];
      if (!coords) return null;
      return { ...cidade, ...coords };
    })
    .filter(Boolean) as CidadeComCoordenadas[];

  const rotas = (apiMapa.rotas || []).map((rota) => ({
    ...rota,
    cor: rota.cor.toLowerCase(),
  }));

  return { cidades, rotas };
}
