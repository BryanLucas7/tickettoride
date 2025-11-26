/**
 * BonusMaiorCaminho - Widget de bônus do maior caminho contínuo
 * 
 * Responsabilidade única: Exibir status do bônus de maior caminho
 */

'use client';

interface BonusMaiorCaminhoProps {
  bonus: boolean;
  tamanho?: number;
}

export function BonusMaiorCaminho({ bonus, tamanho }: BonusMaiorCaminhoProps) {
  return (
    <div className={`
      flex justify-between items-center p-2 rounded
      ${bonus ? 'bg-purple-100 border-2 border-purple-500' : 'bg-gray-100'}
    `}>
      <div className="flex items-center gap-2">
        <span className={`font-semibold ${bonus ? 'text-purple-800' : 'text-gray-600'}`}>
          {bonus ? '🌟' : '➖'} Maior Caminho Contínuo
        </span>
        {tamanho !== undefined && (
          <span className="text-xs text-gray-600">
            ({tamanho} segmentos)
          </span>
        )}
      </div>
      <span className={`text-lg font-bold ${bonus ? 'text-purple-900' : 'text-gray-500'}`}>
        {bonus ? '+10' : '0'}
      </span>
    </div>
  );
}
