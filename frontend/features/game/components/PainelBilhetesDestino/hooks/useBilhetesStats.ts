/**
 * useBilhetesStats - Hook para cálculo de estatísticas de bilhetes
 * 
 * Responsabilidade única: Calcular e memorizar estatísticas de bilhetes
 */

import { useMemo } from 'react';
import type { BilheteDestinoUI, BilhetesStats } from '../types';

export function useBilhetesStats(bilhetes: BilheteDestinoUI[]): BilhetesStats {
  return useMemo(() => {
    const totalBilhetes = bilhetes.length;
    const bilhetesCompletos = bilhetes.filter(b => b.completo).length;
    const bilhetesIncompletos = totalBilhetes - bilhetesCompletos;
    
    const pontosGanhos = bilhetes
      .filter(b => b.completo)
      .reduce((total, b) => total + b.pontos, 0);
    
    const pontosPerdidos = bilhetes
      .filter(b => !b.completo)
      .reduce((total, b) => total + b.pontos, 0);
    
    const pontosTotaisPossiveis = bilhetes.reduce((total, b) => total + b.pontos, 0);
    
    const balanco = pontosGanhos - pontosPerdidos;
    
    const percentualCompleto = totalBilhetes > 0 
      ? Math.round((bilhetesCompletos / totalBilhetes) * 100) 
      : 0;
    
    return {
      totalBilhetes,
      bilhetesCompletos,
      bilhetesIncompletos,
      pontosGanhos,
      pontosPerdidos,
      pontosTotaisPossiveis,
      balanco,
      percentualCompleto
    };
  }, [bilhetes]);
}
