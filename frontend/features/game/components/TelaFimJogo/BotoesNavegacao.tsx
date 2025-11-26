/**
 * BotoesNavegacao - Botões de ação pós-jogo
 * 
 * Responsabilidade única: Renderizar botões de navegação
 */

'use client';

interface BotoesNavegacaoProps {
  onJogarNovamente?: () => void;
  onVoltarMenu?: () => void;
}

export function BotoesNavegacao({ 
  onJogarNovamente, 
  onVoltarMenu 
}: BotoesNavegacaoProps) {
  return (
    <div className="p-6 bg-white bg-opacity-50 border-t-2 border-yellow-400 flex gap-3 justify-center">
      {onJogarNovamente && (
        <button
          onClick={onJogarNovamente}
          className="px-6 py-3 bg-green-500 text-white rounded-lg font-bold text-lg hover:bg-green-600 transition-colors shadow-lg"
        >
          🔄 Jogar Novamente
        </button>
      )}
      
      {onVoltarMenu && (
        <button
          onClick={onVoltarMenu}
          className="px-6 py-3 bg-blue-500 text-white rounded-lg font-bold text-lg hover:bg-blue-600 transition-colors shadow-lg"
        >
          🏠 Voltar ao Menu
        </button>
      )}
    </div>
  );
}
