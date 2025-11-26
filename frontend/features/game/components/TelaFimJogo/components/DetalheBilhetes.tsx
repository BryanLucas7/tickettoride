/**
 * DetalheBilhetes - Exibe bilhetes completos e incompletos
 * 
 * Responsabilidade única: Renderizar seções de bilhetes
 */

'use client';

import type { BilheteResultado } from '../types';

interface DetalheBilhetesProps {
  bilhetesCompletos: BilheteResultado[];
  bilhetesIncompletos: BilheteResultado[];
  pontosBilhetesPositivos: number;
  pontosBilhetesNegativos: number;
}

/**
 * Lista de bilhetes individuais
 */
function ListaBilhetes({ 
  bilhetes, 
  tipo 
}: { 
  bilhetes: BilheteResultado[]; 
  tipo: 'completo' | 'incompleto';
}) {
  const corTexto = tipo === 'completo' ? 'text-green-700' : 'text-red-700';
  const sinal = tipo === 'completo' ? '+' : '-';

  return (
    <>
      {bilhetes.map((bilhete, i) => (
        <div key={i} className={`text-sm ${corTexto} ml-4`}>
          • {bilhete.origem} ↔ {bilhete.destino} ({sinal}{bilhete.pontos})
        </div>
      ))}
    </>
  );
}

export function DetalheBilhetes({
  bilhetesCompletos,
  bilhetesIncompletos,
  pontosBilhetesPositivos,
  pontosBilhetesNegativos
}: DetalheBilhetesProps) {
  return (
    <>
      {/* Bilhetes Completos */}
      <div className="p-2 bg-green-50 rounded">
        <div className="flex justify-between items-center mb-2">
          <span className="font-semibold text-green-800">
            ✅ Bilhetes Completos ({bilhetesCompletos.length})
          </span>
          <span className="text-lg font-bold text-green-900">
            +{pontosBilhetesPositivos}
          </span>
        </div>
        <ListaBilhetes bilhetes={bilhetesCompletos} tipo="completo" />
      </div>
      
      {/* Bilhetes Incompletos */}
      {bilhetesIncompletos.length > 0 && (
        <div className="p-2 bg-red-50 rounded">
          <div className="flex justify-between items-center mb-2">
            <span className="font-semibold text-red-800">
              ❌ Bilhetes Incompletos ({bilhetesIncompletos.length})
            </span>
            <span className="text-lg font-bold text-red-900">
              {pontosBilhetesNegativos}
            </span>
          </div>
          <ListaBilhetes bilhetes={bilhetesIncompletos} tipo="incompleto" />
        </div>
      )}
    </>
  );
}
