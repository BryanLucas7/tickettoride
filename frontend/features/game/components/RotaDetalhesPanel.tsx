/**
 * RotaDetalhesPanel - Painel de detalhes da rota selecionada
 * 
 * Responsabilidade: Exibir informações da rota e permitir conquista
 */

import type { UseGameEngineReturn } from "@/hooks/useGameEngine"
import { buttonClass } from '@/lib/constants/styles'

interface RotaDetalhesPanelProps {
  rotaMapa: {
    comprimento: number
    cor: string
  }
  rotaDoJogo: {
    conquistada?: boolean
    proprietario_nome?: string | null
  } | null | undefined
  game: UseGameEngineReturn
  ehMinhaVez: boolean
  getCoresBg: (cor: string) => string
  getCorTexto: (cor: string) => string
  getLetraCor: (cor: string) => string
}

export function RotaDetalhesPanel({
  rotaMapa,
  rotaDoJogo,
  game,
  ehMinhaVez,
  getCoresBg,
  getCorTexto,
  getLetraCor
}: RotaDetalhesPanelProps) {
  if (rotaDoJogo?.conquistada) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-sm text-green-800">
        Essa rota já foi conquistada por {rotaDoJogo.proprietario_nome}.
      </div>
    )
  }

  if (game.fluxoBilhetesAtivo || game.carregandoBilhetesPreview || game.acaoCartasBloqueiaOutras) {
    return (
      <p className="text-sm text-orange-700 text-center">
        {game.acaoCartasBloqueiaOutras
          ? "Conclua a compra de cartas antes de interagir com rotas."
          : "Conclua a compra de bilhetes antes de interagir com rotas."}
      </p>
    )
  }

  if (!ehMinhaVez) {
    return (
      <p className="text-sm text-gray-600 text-center">
        Aguarde sua vez para conquistar esta rota.
      </p>
    )
  }

  if (game.minhasCartas.length === 0) {
    return (
      <p className="text-sm text-gray-600 text-center">
        Você não tem cartas disponíveis. Compre cartas para poder conquistar rotas.
      </p>
    )
  }

  const cartasNecessarias = rotaMapa.comprimento
  const corRota = rotaMapa.cor
  const rotaEhCinza = corRota.toLowerCase() === "cinza"

  return (
    <div className="space-y-4">
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 text-sm text-purple-800">
        <p className="font-semibold">
          Selecione {cartasNecessarias} carta{cartasNecessarias > 1 ? "s" : ""}{" "}
          {rotaEhCinza ? "da mesma cor à sua escolha" : `na cor ${corRota.toLowerCase()}`}.
        </p>
        <p className="text-xs text-purple-600 mt-1">
          Cartas locomotiva podem substituir qualquer cor{rotaEhCinza ? ", mas cores diferentes não podem ser misturadas." : "."}
        </p>
      </div>

      <div>
        <p className="text-xs text-gray-600 mb-2">Clique nas cartas para selecioná-las:</p>
        <div className="flex flex-wrap gap-2">
          {game.minhasCartas.map((carta, idx) => {
            const selecionada = game.cartasSelecionadas.includes(idx)
            return (
              <button
                key={`rota-card-${idx}-${carta.cor}`}
                type="button"
                onClick={() => game.toggleCartaSelecionada(idx, cartasNecessarias)}
                className={`w-16 h-20 rounded-lg border-2 flex items-center justify-center text-xs font-bold transition-all ${
                  selecionada
                    ? "border-green-600 ring-2 ring-green-300"
                    : "border-gray-300 hover:border-purple-300"
                } ${getCoresBg(carta.cor)} ${getCorTexto(carta.cor)}`}
              >
                {getLetraCor(carta.cor)}
              </button>
            )
          })}
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Cartas selecionadas: {game.cartasSelecionadas.length}/{cartasNecessarias}
        </p>
      </div>

      <div className="flex gap-2 flex-wrap">
        <button
          type="button"
          className={buttonClass('PURPLE', 'MD', 'flex-1 min-w-[180px]')}
          onClick={game.conquistarRota}
          disabled={!game.podeConquistarRota}
        >
          Conquistar rota selecionada
        </button>
        <button
          type="button"
          className="flex-1 min-w-[160px] bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg transition-colors"
          onClick={() => game.setCartasSelecionadas([])}
        >
          Limpar seleção
        </button>
      </div>
    </div>
  )
}
