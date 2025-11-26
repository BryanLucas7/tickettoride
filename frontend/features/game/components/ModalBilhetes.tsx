/**
 * ModalBilhetes - Modal de seleção de bilhetes de destino
 * 
 * Responsabilidade: Interface para selecionar bilhetes durante o fluxo de compra
 */

import type { UseGameEngineReturn } from "@/hooks/useGameEngine"
import { buttonClass } from '@/lib/constants/styles'

interface ModalBilhetesProps {
  game: UseGameEngineReturn
}

export function ModalBilhetes({ game }: ModalBilhetesProps) {
  return (
    <div className="border-2 border-orange-200 rounded-lg p-3 bg-orange-50/60 space-y-4">
      <div className="flex flex-col gap-1">
        <h3 className="font-semibold text-orange-700">Selecionar Bilhetes</h3>
        <p className="text-sm text-gray-600">
          Escolha pelo menos 1 e no máximo 3 bilhetes. Enquanto esta etapa estiver aberta,
          outras ações permanecem bloqueadas para que você possa analisar o mapa e seus
          bilhetes atuais com calma.
        </p>
      </div>

      <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
        {game.bilhetesDisponiveis.map((bilhete) => {
          const selecionado = game.bilhetesSelecionados.includes(bilhete.index)
          return (
            <button
              key={bilhete.index}
              type="button"
              onClick={() => game.toggleBilheteSelecionado(bilhete.index, 0)}
              className={`w-full p-3 rounded-lg border-2 text-left transition-all ${
                selecionado
                  ? "border-orange-600 bg-orange-50"
                  : "border-gray-200 hover:border-orange-300"
              }`}
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-semibold text-gray-900">
                    {bilhete.cidadeOrigem} → {bilhete.cidadeDestino}
                  </p>
                  <p className="text-xs text-gray-600">{bilhete.pontos} pontos</p>
                </div>
                {selecionado && <span className="text-orange-600 text-xl">✓</span>}
              </div>
            </button>
          )
        })}
      </div>

      <p className="text-sm text-gray-600">
        Selecionados: {game.bilhetesSelecionados.length}/3
      </p>

      <button
        type="button"
        onClick={game.confirmarBilhetes}
        disabled={game.bilhetesSelecionados.length === 0}
        className={buttonClass('ORANGE', 'MD', 'w-full')}
      >
        Confirmar escolha ({game.bilhetesSelecionados.length})
      </button>
    </div>
  )
}
