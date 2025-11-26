/**
 * MaiorCaminhoWidget - Exibe o maior caminho contínuo do jogo
 * 
 * Responsabilidade: Renderizar informações sobre o bônus de maior caminho
 */

import { obterCorMapa, type GameState } from "@/types/game"

interface MaiorCaminhoWidgetProps {
  gameState: GameState
}

export function MaiorCaminhoWidget({ gameState }: MaiorCaminhoWidgetProps) {
  return (
    <div className="bg-gradient-to-br from-purple-100 via-purple-50 to-indigo-50 rounded-lg shadow-lg p-4 border-2 border-purple-200">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2 text-purple-900 font-bold text-lg">
          <span className="text-2xl">🚂</span>
          Maior Caminho Contínuo
        </div>
        <span className="text-[11px] uppercase tracking-wide text-purple-600 font-semibold bg-white/70 px-2 py-1 rounded-full">
          Atualiza a cada turno
        </span>
      </div>

      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase font-semibold text-purple-600">Comprimento atual</p>
          <p className="text-4xl font-extrabold text-purple-900">
            {gameState?.maior_caminho?.comprimento ?? 0}
          </p>
          <p className="text-xs text-purple-600">segmentos conectados</p>
        </div>
        <div className="text-right">
          <p className="text-xs uppercase font-semibold text-purple-600">Bônus no fim</p>
          <p className="text-2xl font-bold text-purple-800">+10 pts</p>
        </div>
      </div>

      {gameState?.maior_caminho?.comprimento ? (
        <div className="mt-4">
          <p className="text-xs uppercase text-purple-700 font-semibold">
            {gameState.maior_caminho.lideres.length > 1 ? "Líderes empatados" : "Jogador líder"}
          </p>
          <div className="mt-2 flex flex-wrap gap-2">
            {gameState.maior_caminho.lideres.map((lider) => {
              const corFundo = obterCorMapa(lider.jogador_cor, "#7c3aed")
              return (
                <div
                  key={lider.jogador_id}
                  className="flex items-center gap-2 bg-white/80 border border-purple-100 rounded-full px-3 py-1 shadow-sm"
                >
                  <span
                    className="w-3 h-3 rounded-full border border-white"
                    style={{ backgroundColor: corFundo }}
                  ></span>
                  <div className="text-sm text-purple-900 font-semibold">
                    {lider.jogador_nome}
                  </div>
                </div>
              )
            })}
          </div>
          {gameState.maior_caminho.caminho && gameState.maior_caminho.caminho.length > 0 && (
            <p className="mt-3 text-xs text-purple-800">
              Caminho: {gameState.maior_caminho.caminho.join(" → ")}
            </p>
          )}
        </div>
      ) : (
        <div className="mt-4 bg-white/70 rounded-lg p-3 text-center">
          <p className="text-sm text-purple-700 font-medium">
            Nenhum caminho conectado ainda. Conquiste rotas para assumir a liderança!
          </p>
        </div>
      )}

      <p className="mt-3 text-[11px] text-purple-600 flex items-center gap-2">
        <span className="text-lg">ℹ️</span>
        Sequência contínua sem repetir rotas; quem lidera agora leva o bônus se mantiver até o fim.
      </p>
    </div>
  )
}
