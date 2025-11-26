/**
 * JogoError - Tela de erro do jogo
 * 
 * Responsabilidade única: Exibir mensagem de erro e botão de voltar
 */

'use client';

interface JogoErrorProps {
  mensagem: string;
  onVoltar: () => void;
}

export function JogoError({ mensagem, onVoltar }: JogoErrorProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md">
        <h2 className="text-2xl font-bold text-red-600 mb-4">Erro</h2>
        <p className="text-gray-700 mb-4">{mensagem}</p>
        <button
          onClick={onVoltar}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg"
        >
          Voltar ao Início
        </button>
      </div>
    </div>
  );
}
