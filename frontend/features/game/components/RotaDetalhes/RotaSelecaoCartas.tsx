/**
 * RotaSelecaoCartas - Estado ativo para seleção de cartas e conquista
 * 
 * GRASP - High Cohesion: Focado na interação de seleção de cartas
 * 
 * REFATORAÇÃO DRY: Usa componentes compartilhados SelectionInstructions e CardSelectionGrid
 * eliminando duplicação de código em ~50 linhas
 * 
 * Responsabilidades:
 * - Orquestrar componentes de seleção compartilhados
 * - Botões de ação (conquistar/limpar)
 */

import type { RotaSelecaoCartasProps } from './types'
import { buttonClass } from '@/lib/constants/styles'
import { CardSelectionGrid, SelectionInstructions } from '../shared'

/**
 * Botões de ação
 */
function BotoesAcao({
  podeConquistar,
  onConquistar,
  onLimpar
}: {
  podeConquistar: boolean
  onConquistar: () => void
  onLimpar: () => void
}) {
  return (
    <div className="flex gap-2 flex-wrap">
      <button
        type="button"
        className={buttonClass('PURPLE', 'MD', 'flex-1 min-w-[180px]')}
        onClick={onConquistar}
        disabled={!podeConquistar}
      >
        Conquistar rota selecionada
      </button>
      <button
        type="button"
        className="flex-1 min-w-[160px] bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg transition-colors"
        onClick={onLimpar}
      >
        Limpar seleção
      </button>
    </div>
  )
}

/**
 * Componente principal de seleção de cartas
 * Usa componentes compartilhados para eliminar duplicação
 */
export function RotaSelecaoCartas({
  rotaMapa,
  game
}: RotaSelecaoCartasProps) {
  const cartasNecessarias = rotaMapa.comprimento
  const corRota = rotaMapa.cor
  const rotaEhCinza = corRota.toLowerCase() === "cinza"

  return (
    <div className="space-y-4">
      <SelectionInstructions
        cartasNecessarias={cartasNecessarias}
        corRota={corRota}
        rotaEhCinza={rotaEhCinza}
      />

      <CardSelectionGrid
        cartas={game.minhasCartas}
        cartasSelecionadas={game.cartasSelecionadas}
        cartasNecessarias={cartasNecessarias}
        onToggle={game.toggleCartaSelecionada}
      />

      <BotoesAcao
        podeConquistar={game.podeConquistarRota}
        onConquistar={game.conquistarRota}
        onLimpar={() => game.setCartasSelecionadas([])}
      />
    </div>
  )
}
