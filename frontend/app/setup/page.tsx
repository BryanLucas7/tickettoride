"use client"

/**
 * SetupPage - Configuração inicial da partida
 *
 * Agora o anfitrião define apenas o número de jogadores.
 * Cada jogador entra depois via link e assume seu assento.
 */

import { useCallback, useMemo, useState } from "react"
import { useRouter } from "next/navigation"
import { CORES_DISPONIVEIS } from "@/hooks/usePlayerSetup"
import { useGameSetup } from "@/hooks/useGameSetup"

export default function SetupPage() {
  const router = useRouter()
  const [numeroJogadores, setNumeroJogadores] = useState(2)
  const { criarJogo, criandoJogo } = useGameSetup()

  const jogadoresPadrao = useMemo(
    () =>
      Array.from({ length: numeroJogadores }, (_, i) => ({
        nome: `Jogador ${i + 1}`,
        cor: CORES_DISPONIVEIS[i % CORES_DISPONIVEIS.length]
      })),
    [numeroJogadores]
  )

  const iniciarJogo = useCallback(async () => {
    if (numeroJogadores < 2 || numeroJogadores > 5) {
      alert("Escolha entre 2 e 5 jogadores.")
      return
    }

    try {
      const resultado = await criarJogo(jogadoresPadrao)
      router.push(`/entrar?gameId=${resultado.gameId}`)
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Erro desconhecido"
      alert(errorMessage)
    }
  }, [numeroJogadores, jogadoresPadrao, router, criarJogo])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-xl p-8 space-y-6">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Configurar partida</h1>
            <p className="text-gray-600">
              Defina apenas o número de jogadores. Cada pessoa abrirá uma aba e entrará pelo link
              gerado para escolher seu assento.
            </p>
          </div>

          <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">
            <label className="block text-sm font-semibold text-blue-900 mb-2">
              Quantidade de jogadores (2 a 5)
            </label>
            <div className="flex items-center gap-3">
              <input
                type="range"
                min={2}
                max={5}
                value={numeroJogadores}
                onChange={(e) => setNumeroJogadores(Number(e.target.value))}
                className="flex-1 accent-blue-600"
              />
              <span className="text-lg font-bold text-blue-800 w-10 text-center">
                {numeroJogadores}
              </span>
            </div>
            <p className="text-sm text-blue-800 mt-2">
              Jogadores gerados: {jogadoresPadrao.map((j) => j.nome).join(", ")}
            </p>
          </div>

          <button
            onClick={iniciarJogo}
            disabled={criandoJogo}
            className="w-full px-6 py-3 font-semibold rounded-lg transition-colors bg-blue-600 hover:bg-blue-700 text-white disabled:bg-blue-300"
          >
            {criandoJogo ? "Criando partida..." : "Criar partida e gerar link"}
          </button>

          <button
            onClick={() => router.push("/")}
            className="w-full px-6 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            Voltar
          </button>
        </div>
      </div>
    </div>
  )
}
