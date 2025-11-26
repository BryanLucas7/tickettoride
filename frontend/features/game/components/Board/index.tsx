/**
 * Board - Componente orquestrador refatorado
 * 
 * Princípios GRASP aplicados:
 * - SRP: RouteShape, CityDot, RotaSelecionadaInfo extraídos
 * - Information Expert: Hook useMapaCalculations
 * - Low Coupling: Componentes SVG independentes
 * 
 * Refatoração: 374 linhas → ~120 linhas (orquestrador)
 */

'use client';

import { useCallback, useState } from 'react';
import { RouteShape } from './RouteShape';
import { CityDot } from './CityDot';
import { RotaSelecionadaInfo } from './RotaSelecionadaInfo';
import { useMapaCalculations } from './hooks/useMapaCalculations';
import type { BoardProps, RotaApi } from './types';

// Re-exports
export type { BoardProps, RotaDoJogo, RotaApi, CidadeComCoordenadas, MapaComCoordenadas } from './types';

export default function Board({ 
  mapa, 
  rotasDoJogo = [], 
  rotaSelecionadaId = null, 
  onRotaSelecionada, 
  renderRotaDetalhes 
}: BoardProps) {
  const [cidadeHover, setCidadeHover] = useState<string | null>(null);

  const { 
    encontrarCidade, 
    encontrarRotaDoJogo, 
    calcularPontoMedio 
  } = useMapaCalculations({ mapa, rotasDoJogo });

  const handleRotaClick = useCallback((rota: RotaApi) => {
    const rotaInfo = encontrarRotaDoJogo(rota.id);
    if (rotaInfo?.conquistada) return;

    const novoSelecionado = rotaSelecionadaId === rota.id ? null : rota.id;
    onRotaSelecionada?.(novoSelecionado);
  }, [encontrarRotaDoJogo, onRotaSelecionada, rotaSelecionadaId]);

  // Mapa não disponível
  if (!mapa || mapa.cidades.length === 0 || mapa.rotas.length === 0) {
    return (
      <div className="w-full max-w-7xl mx-auto p-4">
        <div className="bg-white rounded-lg shadow-xl p-6 text-gray-700">
          Mapa não disponível. Recarregue após iniciar o backend para obter a definição canônica.
        </div>
      </div>
    );
  }

  const rotaSelecionada = rotaSelecionadaId
    ? mapa.rotas.find((rota) => rota.id === rotaSelecionadaId) ?? null
    : null;
  const rotaSelecionadaInfo = rotaSelecionada
    ? encontrarRotaDoJogo(rotaSelecionada.id)
    : undefined;

  return (
    <div className="w-full max-w-7xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-xl overflow-hidden">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b-2 border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Mapa do Brasil</h2>
          <div className="flex gap-4 text-sm text-gray-600">
            <span className="bg-gray-100 px-3 py-1 rounded-md font-medium">
              {mapa.cidades.length} cidades
            </span>
            <span className="bg-gray-100 px-3 py-1 rounded-md font-medium">
              {mapa.rotas.length} rotas
            </span>
          </div>
        </div>

        {/* SVG do Mapa */}
        <div className="p-6 bg-sky-50">
          <svg 
            className="w-full h-auto border-2 border-gray-300 rounded-lg bg-sky-100" 
            viewBox="0 0 700 700"
          >
            <defs>
              <filter id="routeBadgeShadow" x="-50%" y="-50%" width="200%" height="200%">
                <feDropShadow dx="0" dy="1" stdDeviation="1.2" floodColor="#000000" floodOpacity="0.25" />
              </filter>
            </defs>
            
            {/* Imagem de fundo */}
            <image
              href="/images/mapa-brasil.png"
              x="0"
              y="0"
              width="700"
              height="700"
              opacity="0.8"
              preserveAspectRatio="xMidYMid slice"
            />
            <rect width="700" height="700" fill="rgba(224, 242, 254, 0.2)" />

            {/* Rotas */}
            {mapa.rotas.map((rota) => {
              const cidadeA = encontrarCidade(rota.cidadeA);
              const cidadeB = encontrarCidade(rota.cidadeB);
              if (!cidadeA || !cidadeB) return null;
              
              return (
                <RouteShape
                  key={rota.id}
                  rota={rota}
                  cidadeA={cidadeA}
                  cidadeB={cidadeB}
                  pontoMedio={calcularPontoMedio(rota)}
                  isSelected={rotaSelecionadaId === rota.id}
                  rotaInfo={encontrarRotaDoJogo(rota.id)}
                  onClick={() => handleRotaClick(rota)}
                />
              );
            })}

            {/* Cidades */}
            {mapa.cidades.map((cidade) => (
              <CityDot
                key={cidade.id}
                cidade={cidade}
                isHover={cidadeHover === cidade.id}
                onHover={setCidadeHover}
              />
            ))}
          </svg>
        </div>

        {/* Painel de Rota Selecionada */}
        {rotaSelecionada && (
          <RotaSelecionadaInfo
            rota={rotaSelecionada}
            rotaInfo={rotaSelecionadaInfo}
            encontrarCidade={encontrarCidade}
            onFechar={() => onRotaSelecionada?.(null)}
            renderRotaDetalhes={renderRotaDetalhes}
          />
        )}
      </div>
    </div>
  );
}
