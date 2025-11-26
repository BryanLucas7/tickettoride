/**
 * RotaSelecionadaInfo - Painel de informações da rota selecionada
 * 
 * Responsabilidade única: Exibir detalhes da rota selecionada
 */

'use client';

import type { ReactNode } from 'react';
import { obterCorHex } from '@/app/data/mapaBrasil';
import type { RotaApi, RotaDoJogo, CidadeComCoordenadas } from './types';

interface RotaSelecionadaInfoProps {
  rota: RotaApi;
  rotaInfo?: RotaDoJogo;
  encontrarCidade: (id: string) => CidadeComCoordenadas | undefined;
  onFechar: () => void;
  renderRotaDetalhes?: (dados: {
    rotaMapa: RotaApi;
    rotaDoJogo?: RotaDoJogo;
  }) => ReactNode;
}

export function RotaSelecionadaInfo({
  rota,
  rotaInfo,
  encontrarCidade,
  onFechar,
  renderRotaDetalhes
}: RotaSelecionadaInfoProps) {
  return (
    <div className="p-6 bg-gray-50 border-t-2 border-gray-200">
      <div className="max-w-2xl mx-auto">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Rota Selecionada</h3>
        
        <div className="grid grid-cols-2 gap-4">
          {/* Cidade de origem */}
          <div>
            <p className="text-sm text-gray-600">De:</p>
            <p className="font-semibold text-gray-900">
              {encontrarCidade(rota.cidadeA)?.nome}
            </p>
          </div>
          
          {/* Cidade de destino */}
          <div>
            <p className="text-sm text-gray-600">Para:</p>
            <p className="font-semibold text-gray-900">
              {encontrarCidade(rota.cidadeB)?.nome}
            </p>
          </div>
          
          {/* Cor da rota */}
          <div>
            <p className="text-sm text-gray-600">Cor:</p>
            <span 
              className="inline-block px-3 py-1 rounded text-white text-xs font-bold uppercase"
              style={{ backgroundColor: obterCorHex(rota.cor) }}
            >
              {rota.cor.toUpperCase()}
            </span>
          </div>
          
          {/* Comprimento */}
          <div>
            <p className="text-sm text-gray-600">Comprimento:</p>
            <p className="font-semibold text-gray-900">
              {rota.comprimento} vagões
            </p>
          </div>
          
          {/* Informações do proprietário */}
          <div className="col-span-2 mt-2 pt-4 border-t-2 border-gray-300 space-y-4">
            {rotaInfo?.conquistada && rotaInfo.proprietario_nome ? (
              <div>
                <p className="text-sm text-gray-600 mb-2">Conquistada por:</p>
                <div
                  className="flex items-center gap-3 bg-white p-3 rounded-lg border-2"
                  style={{ borderColor: obterCorHex(rotaInfo.proprietario_cor || undefined) }}
                >
                  <div
                    className="w-8 h-8 rounded-full"
                    style={{ backgroundColor: obterCorHex(rotaInfo.proprietario_cor || undefined) }}
                  />
                  <span className="font-bold text-lg text-gray-900">
                    {rotaInfo.proprietario_nome}
                  </span>
                  <span className="ml-auto text-green-600 font-semibold">✓ Conquistada</span>
                </div>
              </div>
            ) : (
              <p className="text-gray-500 italic text-center">
                🔓 Rota disponível para conquista
              </p>
            )}

            {renderRotaDetalhes?.({ rotaMapa: rota, rotaDoJogo: rotaInfo })}
          </div>
        </div>
        
        {/* Botão fechar */}
        <button
          onClick={onFechar}
          className="mt-4 w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
        >
          Fechar
        </button>
      </div>
    </div>
  );
}
