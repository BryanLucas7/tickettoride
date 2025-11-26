/**
 * CardSelectionGrid - Grid de cartas selecionáveis
 * 
 * REFATORAÇÃO DRY: Extraído de RotaDetalhesPanel e RotaSelecaoCartas
 * para eliminar duplicação de código.
 * 
 * GRASP - High Cohesion: Focado apenas em renderização do grid
 * GRASP - Low Coupling: Não depende de estado externo específico
 */

import { useCardColors } from '@/hooks/useCardColors'

// ============================================
// TIPOS
// ============================================

export interface CardSelectionGridProps {
  /** Lista de cartas para exibir */
  cartas: Array<{ cor: string }>
  /** Índices das cartas selecionadas */
  cartasSelecionadas: number[]
  /** Número máximo de cartas a selecionar */
  cartasNecessarias: number
  /** Callback para toggle de seleção */
  onToggle: (index: number, limite: number) => void
  /** Texto de instrução (opcional) */
  instrucaoTexto?: string
  /** Mostrar contador de selecionadas */
  mostrarContador?: boolean
}

// ============================================
// COMPONENTE PRINCIPAL
// ============================================

/**
 * Grid de cartas selecionáveis para conquista de rotas
 * 
 * @example
 * ```tsx
 * <CardSelectionGrid
 *   cartas={minhasCartas}
 *   cartasSelecionadas={selecionadas}
 *   cartasNecessarias={rotaComprimento}
 *   onToggle={(idx, limite) => toggleCarta(idx, limite)}
 * />
 * ```
 */
export function CardSelectionGrid({
  cartas,
  cartasSelecionadas,
  cartasNecessarias,
  onToggle,
  instrucaoTexto = "Clique nas cartas para selecioná-las:",
  mostrarContador = true
}: CardSelectionGridProps) {
  // Usa hook centralizado de cores
  const { getCoresBg, getCorTexto, getLetraCor } = useCardColors()
  
  return (
    <div>
      <p className="text-xs text-gray-600 mb-2">{instrucaoTexto}</p>
      <div className="flex flex-wrap gap-2">
        {cartas.map((carta, idx) => {
          const selecionada = cartasSelecionadas.includes(idx)
          return (
            <button
              key={`card-selection-${idx}-${carta.cor}`}
              type="button"
              onClick={() => onToggle(idx, cartasNecessarias)}
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
      {mostrarContador && (
        <p className="text-xs text-gray-500 mt-2">
          Cartas selecionadas: {cartasSelecionadas.length}/{cartasNecessarias}
        </p>
      )}
    </div>
  )
}

// ============================================
// COMPONENTE DE INSTRUÇÕES
// ============================================

export interface SelectionInstructionsProps {
  /** Número de cartas necessárias */
  cartasNecessarias: number
  /** Cor da rota */
  corRota: string
  /** Se a rota é cinza (qualquer cor) */
  rotaEhCinza: boolean
}

/**
 * Instruções de seleção de cartas para conquista de rota
 */
export function SelectionInstructions({
  cartasNecessarias,
  corRota,
  rotaEhCinza
}: SelectionInstructionsProps) {
  return (
    <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 text-sm text-purple-800">
      <p className="font-semibold">
        Selecione {cartasNecessarias} carta{cartasNecessarias > 1 ? "s" : ""}{" "}
        {rotaEhCinza ? "da mesma cor à sua escolha" : `na cor ${corRota.toLowerCase()}`}.
      </p>
      <p className="text-xs text-purple-600 mt-1">
        Cartas locomotiva podem substituir qualquer cor
        {rotaEhCinza ? ", mas cores diferentes não podem ser misturadas." : "."}
      </p>
    </div>
  )
}

export default CardSelectionGrid
