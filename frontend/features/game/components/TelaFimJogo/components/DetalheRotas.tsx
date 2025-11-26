/**
 * DetalheRotas - Exibe pontos obtidos por rotas conquistadas
 * 
 * Responsabilidade única: Renderizar seção de pontos de rotas
 */

'use client';

interface DetalheRotasProps {
  pontosRotas: number;
}

export function DetalheRotas({ pontosRotas }: DetalheRotasProps) {
  return (
    <div className="flex justify-between items-center p-2 bg-blue-50 rounded">
      <span className="font-semibold text-blue-800">🛤️ Rotas Conquistadas</span>
      <span className="text-lg font-bold text-blue-900">+{pontosRotas}</span>
    </div>
  );
}
