/**
 * SelecionadosIndicator - Indicador de bilhetes selecionados
 * 
 * Responsabilidade única: Mostrar status de seleção
 */

'use client';

interface SelecionadosIndicatorProps {
  quantidadeSelecionada: number;
  maximo: number;
  minimo: number;
}

export function SelecionadosIndicator({ 
  quantidadeSelecionada, 
  maximo,
  minimo 
}: SelecionadosIndicatorProps) {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
      <p className="text-sm text-blue-800">
        <strong>Bilhetes selecionados:</strong> {quantidadeSelecionada} de {maximo} (mínimo {minimo})
      </p>
    </div>
  );
}
