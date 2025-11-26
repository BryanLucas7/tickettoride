/**
 * ResumoMao - Resumo estatístico da mão de cartas
 * 
 * Responsabilidade única: Exibir estatísticas da mão
 */

'use client';

interface ResumoMaoProps {
  totalCartas: number;
  totalCores: number;
  modoSelecao: boolean;
  cartasSelecionadas: number;
}

export function ResumoMao({
  totalCartas,
  totalCores,
  modoSelecao,
  cartasSelecionadas
}: ResumoMaoProps) {
  if (totalCartas === 0) return null;
  
  return (
    <div className="border-t-2 border-gray-200 pt-3 mt-3">
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div className="bg-gray-50 p-2 rounded">
          <span className="text-gray-600">Total de Cartas:</span>
          <span className="font-bold ml-2">{totalCartas}</span>
        </div>
        <div className="bg-gray-50 p-2 rounded">
          <span className="text-gray-600">Cores Diferentes:</span>
          <span className="font-bold ml-2">{totalCores}</span>
        </div>
      </div>
      
      {modoSelecao && (
        <div className="mt-2 bg-blue-50 border-l-4 border-blue-500 p-2 text-sm text-blue-800">
          💡 Clique nas cartas para selecioná-las ({cartasSelecionadas} selecionadas)
        </div>
      )}
    </div>
  );
}
