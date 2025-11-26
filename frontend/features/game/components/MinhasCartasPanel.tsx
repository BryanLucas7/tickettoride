/**
 * MinhasCartasPanel - Painel que exibe as cartas do jogador
 * 
 * Responsabilidade: Renderizar as cartas na mão do jogador
 */

import MaoCartas, { CorCarta, type CartaVagao as MaoCartaVagao } from "./MaoCartas"

interface CartaSimples {
  cor: string
}

interface MinhasCartasPanelProps {
  jogadorNome: string
  cartas: CartaSimples[]
}

/**
 * Converte string de cor para enum CorCarta
 */
function converterParaCorCarta(cor: string): CorCarta {
  const corUpper = cor.toUpperCase()
  if (corUpper in CorCarta) {
    return CorCarta[corUpper as keyof typeof CorCarta]
  }
  return CorCarta.LOCOMOTIVA
}

export function MinhasCartasPanel({ jogadorNome, cartas }: MinhasCartasPanelProps) {
  return (
    <div className="mt-4 bg-white rounded-lg shadow-xl p-4">
      <h2 className="text-xl font-bold mb-4 text-gray-900">Suas Cartas</h2>
      {cartas.length > 0 ? (
        <MaoCartas
          jogadorNome={jogadorNome}
          cartas={cartas.map((c, i): MaoCartaVagao => ({
            id: `carta-${i}`,
            cor: converterParaCorCarta(c.cor),
          }))}
          modoSelecao={false}
        />
      ) : (
        <div className="text-center py-8 text-gray-500">
          <p>Você ainda não tem cartas</p>
          <p className="text-sm mt-2">Compre cartas durante seu turno</p>
        </div>
      )}
    </div>
  )
}
