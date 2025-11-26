/**
 * PainelBilhetesDestino - Componente orquestrador refatorado
 * 
 * Princípios GRASP aplicados:
 * - SRP: Componentes extraídos com responsabilidade única
 * - Information Expert: Hook calcula estatísticas
 * - Protected Variations: Modo secreto encapsulado
 * 
 * Refatoração: 304 linhas → ~70 linhas (orquestrador)
 */

'use client';

import { useState } from 'react';
import { PainelBilhetesSecreto } from './PainelBilhetesSecreto';
import { BilheteCard } from './BilheteCard';
import { ResumoBilhetes } from './ResumoBilhetes';
import { useBilhetesStats } from './hooks/useBilhetesStats';
import type { PainelBilhetesDestinoProps } from './types';

// Re-exportar tipos
export type { BilheteDestinoUI, PainelBilhetesDestinoProps, BilhetesStats } from './types';

export default function PainelBilhetesDestino({
  bilhetes,
  jogadorNome,
  modoSecreto = true,
  isExpanded = true,
  mostrarStatus = true
}: PainelBilhetesDestinoProps) {
  const [expandido, setExpandido] = useState(isExpanded);
  const stats = useBilhetesStats(bilhetes);
  
  // Modo secreto: esconde detalhes
  if (modoSecreto && bilhetes.length > 0) {
    return (
      <PainelBilhetesSecreto 
        jogadorNome={jogadorNome} 
        totalBilhetes={stats.totalBilhetes} 
      />
    );
  }
  
  return (
    <div className="bg-gradient-to-br from-purple-50 to-indigo-100 rounded-lg shadow-lg border-2 border-purple-300">
      {/* Cabeçalho */}
      <div
        className="flex items-center justify-between p-4 cursor-pointer hover:bg-purple-100 transition-colors rounded-t-lg"
        onClick={() => setExpandido(!expandido)}
      >
        <div className="flex items-center gap-3">
          <span className="text-3xl">🎫</span>
          <div>
            <h3 className="font-bold text-lg text-purple-900">
              Bilhetes de Destino - {jogadorNome}
            </h3>
            <p className="text-sm text-purple-700">
              {stats.totalBilhetes} bilhetes | {stats.bilhetesCompletos} completos
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          {/* Indicador de pontos */}
          <div className="text-right mr-2">
            <div className="text-sm font-semibold text-green-600">
              +{stats.pontosGanhos} pts
            </div>
            {stats.pontosPerdidos > 0 && (
              <div className="text-xs font-semibold text-red-600">
                -{stats.pontosPerdidos} pts
              </div>
            )}
          </div>
          
          {/* Seta de expansão */}
          <span className={`text-2xl transition-transform ${expandido ? 'rotate-180' : ''}`}>
            ▼
          </span>
        </div>
      </div>
      
      {/* Conteúdo expandido */}
      {expandido && (
        <div className="p-4 pt-0">
          {bilhetes.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <span className="text-4xl block mb-2">🎫</span>
              <p>Nenhum bilhete de destino</p>
            </div>
          ) : (
            <>
              {/* Lista de bilhetes */}
              <div className="space-y-3 mb-4">
                {bilhetes.map((bilhete) => (
                  <BilheteCard
                    key={bilhete.id}
                    bilhete={bilhete}
                    mostrarStatus={mostrarStatus}
                  />
                ))}
              </div>
              
              {/* Resumo estatístico */}
              <ResumoBilhetes stats={stats} />
            </>
          )}
        </div>
      )}
    </div>
  );
}
