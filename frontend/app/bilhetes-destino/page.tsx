"use client"

/**
 * BilhetesDestinoPage - Página de seleção inicial de bilhetes
 * 
 * Refatorada seguindo SRP:
 * - Lógica de negócio extraída para hook useBilhetesFlow
 * - Componentes de UI extraídos para pasta components/
 */

import { useBilhetesFlow } from "./hooks/useBilhetesFlow"
import { JogadorHeader } from "./components/JogadorHeader"
import { BilheteSelecaoCard } from "./components/BilheteSelecaoCard"
import { SelecionadosIndicator } from "./components/SelecionadosIndicator"

export default function BilhetesDestinoPage() {
  const {
    jogador,
    bilhetesDisponiveis,
    carregando,
    isValidSelection,
    isSelected,
    quantidadeSelecionada,
    toggleBilhete,
    confirmarSelecao
  } = useBilhetesFlow()

  if (carregando) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-2xl font-semibold text-gray-700">Carregando bilhetes...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <JogadorHeader
            jogadorNome={jogador?.nome ?? "Jogador"}
            jogadorCor={jogador?.cor ?? ""}
            jogadorAtualIndex={0}
            totalJogadores={1}
          />

          <div className="space-y-4 mb-8">
            {bilhetesDisponiveis.map((bilhete) => (
              <BilheteSelecaoCard
                key={bilhete.id}
                bilhete={bilhete}
                selecionado={isSelected(bilhete.id)}
                onToggle={() => toggleBilhete(bilhete.id)}
              />
            ))}
          </div>

          <SelecionadosIndicator 
            quantidadeSelecionada={quantidadeSelecionada}
            maximo={3}
            minimo={2}
          />

          <button
            onClick={confirmarSelecao}
            disabled={!isValidSelection}
            className={`
              w-full px-6 py-4 font-semibold text-lg rounded-lg transition-colors
              ${isValidSelection
                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }
            `}
          >
            Ir para o jogo
          </button>
        </div>
      </div>
    </div>
  )
}
