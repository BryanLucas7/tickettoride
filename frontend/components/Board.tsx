"use client"

import { useState, type ReactNode } from 'react'
import { CIDADES, ROTAS, CORES, type Cidade, type Rota } from '@/app/data/mapaBrasil'

// Interface para rota com informações do jogo
interface RotaDoJogo {
  id: string
  cidadeA: string
  cidadeB: string
  cor: string
  comprimento: number
  proprietario_id: string | null
  proprietario_nome: string | null
  proprietario_cor: string | null
  conquistada: boolean
}

interface BoardProps {
  rotasDoJogo?: RotaDoJogo[]
  rotaSelecionadaId?: string | null
  onRotaSelecionada?: (rotaId: string | null) => void
  renderRotaDetalhes?: (dados: {
    rotaMapa: Rota
    rotaDoJogo?: RotaDoJogo
  }) => ReactNode
}

export default function Board({ rotasDoJogo = [], rotaSelecionadaId = null, onRotaSelecionada, renderRotaDetalhes }: BoardProps) {
  const [cidadeHover, setCidadeHover] = useState<string | null>(null)

  // Função para encontrar informações de uma rota do jogo
  const encontrarRotaDoJogo = (rotaId: string): RotaDoJogo | undefined => {
    return rotasDoJogo.find(r => r.id === rotaId)
  }


  
  const encontrarCidade = (id: string): Cidade | undefined => {
    return CIDADES.find(c => c.id === id);
  };

  const calcularPontoMedio = (rota: Rota) => {
    const cidadeA = encontrarCidade(rota.cidadeA);
    const cidadeB = encontrarCidade(rota.cidadeB);
    if (!cidadeA || !cidadeB) return { x: 0, y: 0 };
    return {
      x: (cidadeA.x + cidadeB.x) / 2,
      y: (cidadeA.y + cidadeB.y) / 2,
    };
  };

  const handleRotaClick = (rota: Rota) => {
    const rotaInfo = encontrarRotaDoJogo(rota.id)
    if (rotaInfo?.conquistada) {
      return
    }

    const novoSelecionado = rotaSelecionadaId === rota.id ? null : rota.id
    onRotaSelecionada?.(novoSelecionado)
  }

  const rotaSelecionada = rotaSelecionadaId
    ? ROTAS.find((rota) => rota.id === rotaSelecionadaId) ?? null
    : null
  const rotaSelecionadaInfo = rotaSelecionada
    ? encontrarRotaDoJogo(rotaSelecionada.id)
    : undefined

  return (
    <div className="w-full max-w-7xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-xl overflow-hidden">
        <div className="flex justify-between items-center p-6 border-b-2 border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Mapa do Brasil</h2>
          <div className="flex gap-4 text-sm text-gray-600">
            <span className="bg-gray-100 px-3 py-1 rounded-md font-medium">
              {CIDADES.length} cidades
            </span>
            <span className="bg-gray-100 px-3 py-1 rounded-md font-medium">
              {ROTAS.length} rotas
            </span>
          </div>
        </div>

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
            {/* Imagem de fundo do mapa do Brasil */}
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

            {ROTAS.map((rota) => {
              const cidadeA = encontrarCidade(rota.cidadeA);
              const cidadeB = encontrarCidade(rota.cidadeB);
              if (!cidadeA || !cidadeB) return null;
              
              const pontoMedio = calcularPontoMedio(rota);
              const isSelected = rotaSelecionadaId === rota.id
              const isWhiteRoute = rota.cor === 'BRANCO'
              
              // Busca informações da rota do jogo (proprietário)
              const rotaInfo = encontrarRotaDoJogo(rota.id);
              const conquistada = rotaInfo?.conquistada || false;
              const corProprietario = rotaInfo?.proprietario_cor;
              const numeroTextColor = isWhiteRoute ? CORES.PRETO : CORES[rota.cor]
              const numeroTextStroke = 'none'
              const numeroTextStrokeWidth = 0
              const circleFillColor = conquistada && corProprietario ? corProprietario : 'white'
              const circleStrokeColor = isWhiteRoute ? '#111827' : CORES[rota.cor]
              const circleFilter = isWhiteRoute ? 'url(#routeBadgeShadow)' : undefined

              return (
                <g key={rota.id}>
                  {/* Borda do proprietário (se conquistada) */}
                  {conquistada && corProprietario && (
                    <line
                      x1={cidadeA.x}
                      y1={cidadeA.y}
                      x2={cidadeB.x}
                      y2={cidadeB.y}
                      stroke={corProprietario}
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
                    stroke={CORES[rota.cor]}
                    strokeWidth={isSelected ? "8" : "6"}
                    strokeLinecap="round"
                    className="cursor-pointer transition-all hover:opacity-80"
                    onClick={() => handleRotaClick(rota)}
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
                    onClick={() => handleRotaClick(rota)}
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
                    stroke={numeroTextStroke}
                    strokeWidth={numeroTextStrokeWidth}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="pointer-events-none"
                  >
                    {rota.comprimento}
                  </text>
                </g>
              );
            })}

            {CIDADES.map((cidade) => (
              <g 
                key={cidade.id}
                onMouseEnter={() => setCidadeHover(cidade.id)}
                onMouseLeave={() => setCidadeHover(null)}
              >
                <circle
                  cx={cidade.x}
                  cy={cidade.y}
                  r={cidadeHover === cidade.id ? "8" : "6"}
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
            ))}
          </svg>
        </div>

        {rotaSelecionada && (
          <div className="p-6 bg-gray-50 border-t-2 border-gray-200">
            <div className="max-w-2xl mx-auto">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Rota Selecionada</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">De:</p>
                  <p className="font-semibold text-gray-900">
                    {encontrarCidade(rotaSelecionada.cidadeA)?.nome}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Para:</p>
                  <p className="font-semibold text-gray-900">
                    {encontrarCidade(rotaSelecionada.cidadeB)?.nome}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Cor:</p>
                  <span 
                    className="inline-block px-3 py-1 rounded text-white text-xs font-bold uppercase"
                    style={{ backgroundColor: CORES[rotaSelecionada.cor] }}
                  >
                    {rotaSelecionada.cor}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Comprimento:</p>
                  <p className="font-semibold text-gray-900">
                    {rotaSelecionada.comprimento} vagões
                  </p>
                </div>
                
                {/* Informações do proprietário */}
                <div className="col-span-2 mt-2 pt-4 border-t-2 border-gray-300 space-y-4">
                  {rotaSelecionadaInfo?.conquistada && rotaSelecionadaInfo.proprietario_nome ? (
                    <div>
                      <p className="text-sm text-gray-600 mb-2">Conquistada por:</p>
                      <div
                        className="flex items-center gap-3 bg-white p-3 rounded-lg border-2"
                        style={{ borderColor: rotaSelecionadaInfo.proprietario_cor || '#9CA3AF' }}
                      >
                        <div
                          className="w-8 h-8 rounded-full"
                          style={{ backgroundColor: rotaSelecionadaInfo.proprietario_cor || '#9CA3AF' }}
                        />
                        <span className="font-bold text-lg text-gray-900">
                          {rotaSelecionadaInfo.proprietario_nome}
                        </span>
                        <span className="ml-auto text-green-600 font-semibold">✓ Conquistada</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-500 italic text-center">
                      🔓 Rota disponível para conquista
                    </p>
                  )}

                  {renderRotaDetalhes?.({ rotaMapa: rotaSelecionada, rotaDoJogo: rotaSelecionadaInfo })}
                </div>
              </div>
              <button
                onClick={() => onRotaSelecionada?.(null)}
                className="mt-4 w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                Fechar
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}