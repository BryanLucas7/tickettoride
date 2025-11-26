/**
 * GameHeader - Cabeçalho do jogo com status e navegação
 * 
 * Responsabilidade: Exibir título, botão de sair e mensagem de status
 */

interface GameHeaderProps {
  mensagem: string
  ehMinhaVez: boolean
  onSair: () => void
}

export function GameHeader({ mensagem, ehMinhaVez, onSair }: GameHeaderProps) {
  return (
    <div className="bg-white rounded-lg shadow-xl p-4 mb-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">🎫 Ticket to Ride - Brasil</h1>
        <button
          onClick={onSair}
          className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
        >
          Sair
        </button>
      </div>

      {/* Mensagem de status */}
      <div
        className={`mt-4 border-l-4 p-4 rounded ${
          ehMinhaVez
            ? "bg-green-50 border-green-500"
            : "bg-blue-50 border-blue-500"
        }`}
      >
        <p className="text-lg font-semibold">{mensagem}</p>
      </div>
    </div>
  )
}
