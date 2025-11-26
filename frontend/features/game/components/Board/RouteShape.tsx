/**
 * RouteShape - Representação visual de uma rota no mapa
 * 
 * Responsabilidade única: Renderizar uma rota SVG
 */

'use client';

import { memo } from 'react';
import {
  type CidadeComCoordenadas,
  type RotaApi,
  CORES_HEX,
  obterCorHex,
} from '@/app/data/mapaBrasil';
import type { RotaDoJogo, PontoMapa } from './types';

export interface RouteShapeProps {
  rota: RotaApi;
  cidadeA: CidadeComCoordenadas;
  cidadeB: CidadeComCoordenadas;
  pontoMedio: PontoMapa;
  isSelected: boolean;
  rotaInfo?: RotaDoJogo;
  onClick: () => void;
}

export const RouteShape = memo(function RouteShape({
  rota,
  cidadeA,
  cidadeB,
  pontoMedio,
  isSelected,
  rotaInfo,
  onClick,
}: RouteShapeProps) {
  const corNormalizada = rota.cor.toLowerCase();
  const corHex = obterCorHex(corNormalizada);
  const isWhiteRoute = corNormalizada === 'branco';

  const conquistada = rotaInfo?.conquistada || false;
  const corProprietarioHex = rotaInfo?.proprietario_cor 
    ? obterCorHex(rotaInfo.proprietario_cor) 
    : null;
  
  const numeroTextColor = isWhiteRoute ? CORES_HEX.preto : corHex;
  const circleFillColor = conquistada && corProprietarioHex 
    ? corProprietarioHex 
    : 'white';
  const circleStrokeColor = isWhiteRoute ? CORES_HEX.preto : corHex;
  const circleFilter = isWhiteRoute ? 'url(#routeBadgeShadow)' : undefined;

  return (
    <g>
      {/* Borda do proprietário (se conquistada) */}
      {conquistada && corProprietarioHex && (
        <line
          x1={cidadeA.x}
          y1={cidadeA.y}
          x2={cidadeB.x}
          y2={cidadeB.y}
          stroke={corProprietarioHex}
          strokeWidth="12"
          strokeLinecap="round"
          opacity="0.5"
          className="pointer-events-none"
        />
      )}
      
      {/* Linha principal da rota */}
      <line
        x1={cidadeA.x}
        y1={cidadeA.y}
        x2={cidadeB.x}
        y2={cidadeB.y}
        stroke={corHex}
        strokeWidth={isSelected ? "8" : "6"}
        strokeLinecap="round"
        className="cursor-pointer transition-all hover:opacity-80"
        onClick={onClick}
      />
      
      {/* Círculo central */}
      <circle
        cx={pontoMedio.x}
        cy={pontoMedio.y}
        r="10"
        fill={circleFillColor}
        stroke={circleStrokeColor}
        strokeWidth="2"
        filter={circleFilter}
        onClick={onClick}
        className="cursor-pointer"
      />
      
      {/* Texto do comprimento */}
      <text
        x={pontoMedio.x}
        y={pontoMedio.y}
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize="14"
        fontWeight="bold"
        fill={numeroTextColor}
        stroke="none"
        strokeWidth={0}
        strokeLinecap="round"
        strokeLinejoin="round"
        className="pointer-events-none"
      >
        {rota.comprimento}
      </text>
    </g>
  );
});
