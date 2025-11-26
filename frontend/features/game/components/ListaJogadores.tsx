/**
 * ListaJogadores - Lista de jogadores com status
 * 
 * Responsabilidade: Exibir informações de todos os jogadores na partida
 */

import type { GameState, Jogador } from "@/types/game"

interface ListaJogadoresProps {
  gameState: GameState
  jogadorAtualId: string
  getCoresBg: (cor: string) => string
}

export function ListaJogadores({ gameState, jogadorAtualId, getCoresBg }: ListaJogadoresProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-4">
      <h2 className="text-xl font-bold mb-4 text-gray-900">Jogadores</h2>
      <div className="space-y-3">
        {gameState.jogadores.map((jogador: Jogador) => (
          <div
            key={jogador.id}
            className={`p-4 rounded-lg border-2 transition-all ${
              jogador.id === gameState.jogador_atual_id
                ? "border-blue-500 bg-blue-50"
                : "border-gray-200 bg-gray-50"
            } ${jogador.id === jogadorAtualId ? "ring-2 ring-green-400" : ""}`}
          >
            <div className="flex items-center gap-3 mb-2">
              <div className={`w-10 h-10 rounded-full ${getCoresBg(jogador.cor)}`}></div>
              <div className="flex-1">
                <h3 className="font-bold text-gray-900">
                  {jogador.nome}
                  <span className="ml-2 inline-flex gap-1">
                    {jogador.id === jogadorAtualId && (
                      <span className="text-xs bg-green-600 text-white px-2 py-1 rounded-full">
                        VOCÊ
                      </span>
                    )}
                    {jogador.id === gameState.jogador_atual_id && (
                      <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded-full">
                        VEZ ATUAL
                      </span>
                    )}
                  </span>
                </h3>
                <p className="text-xs text-gray-500 uppercase">{jogador.cor}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="text-gray-600">Pontuação:</span>
                <span className="ml-2 font-bold text-lg">{jogador.pontos}</span>
              </div>
              <div>
                <span className="text-gray-600">Vagões:</span>
                <span className="ml-2 font-semibold">{jogador.trens_disponiveis}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
