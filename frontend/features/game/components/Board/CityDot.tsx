/**
 * CityDot - Representação visual de uma cidade no mapa
 * 
 * Responsabilidade única: Renderizar um ponto de cidade SVG
 */

'use client';

import { memo } from 'react';
import type { CidadeComCoordenadas } from './types';

export interface CityDotProps {
  cidade: CidadeComCoordenadas;
  isHover: boolean;
  onHover: (id: string | null) => void;
}

export const CityDot = memo(function CityDot({ 
  cidade, 
  isHover, 
  onHover 
}: CityDotProps) {
  return (
    <g
      onMouseEnter={() => onHover(cidade.id)}
      onMouseLeave={() => onHover(null)}
    >
      <circle
        cx={cidade.x}
        cy={cidade.y}
        r={isHover ? "8" : "6"}
        fill="#1E40AF"
        stroke="white"
        strokeWidth="2"
        className="cursor-pointer transition-all"
      />
      
      <text
        x={cidade.x}
        y={cidade.y - 20}
        textAnchor="middle"
        fontSize="12"
        fontWeight="bold"
        fill="#1F2937"
        className="pointer-events-none"
        style={{ textShadow: '1px 1px 2px white, -1px -1px 2px white' }}
      >
        {cidade.nome}
      </text>
    </g>
  );
});
