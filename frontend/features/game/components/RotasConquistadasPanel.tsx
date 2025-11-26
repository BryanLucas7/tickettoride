/**
 * RotasConquistadasPanel - Lista de rotas conquistadas pelo jogador
 * 
 * Responsabilidade: Exibir rotas conquistadas com pontuação
 */

interface RotaConquistada {
  id: string
  origem: string
  destino: string
  comprimento: number
  pontos: number
}

interface RotasConquistadasPanelProps {
  rotasConquistadas: RotaConquistada[]
  totalPontos: number
}

export function RotasConquistadasPanel({ rotasConquistadas, totalPontos }: RotasConquistadasPanelProps) {
  return (
    <div className="mt-4 bg-white rounded-lg shadow-xl p-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-3">
        <h2 className="text-xl font-bold text-gray-900">Rotas Conquistadas</h2>
        <span className="text-sm font-semibold text-green-700">
          Pontos em rotas: {totalPontos}
        </span>
      </div>
      {rotasConquistadas.length === 0 ? (
        <p className="text-sm text-gray-500">
          Ainda não há rotas conquistadas. Use cartas para dominar o mapa!
        </p>
      ) : (
        <ul className="space-y-2">
          {rotasConquistadas.map((rota) => (
            <li
              key={rota.id}
              className="flex items-center justify-between rounded-lg border border-green-100 bg-green-50 px-3 py-2 text-sm"
            >
              <div className="flex flex-col">
                <span className="font-semibold text-gray-800">
                  {rota.origem} → {rota.destino}
                </span>
                <span className="text-xs text-gray-600">
                  {rota.comprimento} vagões
                </span>
              </div>
              <span className="text-sm font-bold text-green-700">+{rota.pontos} pts</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
