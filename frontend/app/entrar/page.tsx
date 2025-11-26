"use client"

import { useCallback, useEffect, useMemo, useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { gameApi, ApiError } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import type { JogadorStorage } from "@/types/api"

type PlayerOption = JogadorStorage

export default function EntrarPage() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const prefilledGameId = searchParams.get("gameId") ?? ""
  const [codigoPartida, setCodigoPartida] = useState(prefilledGameId)
  const [jogadores, setJogadores] = useState<PlayerOption[]>([])
  const [selectedPlayerId, setSelectedPlayerId] = useState<string>("")
  const [mensagem, setMensagem] = useState<string | null>(null)
  const [erro, setErro] = useState<string | null>(null)
  const [carregando, setCarregando] = useState(false)
  const [baseUrl, setBaseUrl] = useState("")

  useEffect(() => {
    if (typeof window !== "undefined") {
      setBaseUrl(window.location.origin)
    }
  }, [])

  const shareLink = useMemo(() => {
    if (!codigoPartida) return ""
    const host = baseUrl || "http://localhost:3000"
    return `${host}/entrar?gameId=${codigoPartida}`
  }, [baseUrl, codigoPartida])

  const buscarPartida = useCallback(async (codigo?: string) => {
    const idParaBuscar = (codigo ?? codigoPartida).trim()
    if (!idParaBuscar) {
      setErro("Informe o código da partida para continuar")
      return
    }

    setErro(null)
    setMensagem(null)
    setCarregando(true)

    try {
      const estado = await gameApi.getGameState(idParaBuscar)
      const jogadoresNormalizados: PlayerOption[] = (estado.jogadores || []).map((jogador) => ({
        id: String(jogador.id),
        nome: jogador.nome,
        cor: String(jogador.cor).toLowerCase(),
      }))

      storageService.setGameData(idParaBuscar, jogadoresNormalizados)
      setJogadores(jogadoresNormalizados)
      setMensagem("Partida encontrada! Escolha seu jogador para entrar.")

      if (selectedPlayerId && !jogadoresNormalizados.some((j) => j.id === selectedPlayerId)) {
        setSelectedPlayerId("")
      }
    } catch (error) {
      console.error("Erro ao buscar partida:", error)

      if (error instanceof ApiError) {
        setErro(error.message)
      } else {
        setErro("Não foi possível localizar a partida. Verifique o código e tente novamente.")
      }

      setJogadores([])
    } finally {
      setCarregando(false)
    }
  }, [codigoPartida, selectedPlayerId])

  useEffect(() => {
    if (prefilledGameId) {
      buscarPartida(prefilledGameId)
    }
  }, [prefilledGameId, buscarPartida])

  const copiarLink = useCallback(async () => {
    if (!shareLink || typeof navigator === "undefined" || !navigator.clipboard) {
      setMensagem("Copie o link manualmente: " + shareLink)
      return
    }

    try {
      await navigator.clipboard.writeText(shareLink)
      setMensagem("Link copiado! Compartilhe com os outros jogadores.")
    } catch {
      setMensagem("Não foi possível copiar automaticamente. Copie o link manualmente.")
    }
  }, [shareLink])

  const entrarComoJogador = useCallback(async () => {
    const codigo = codigoPartida.trim()
    if (!codigo) {
      setErro("Informe o código da partida para continuar")
      return
    }

    const jogadorSelecionado = jogadores.find((j) => j.id === selectedPlayerId)
    if (!jogadorSelecionado) {
      setErro("Selecione qual jogador você é nesta partida")
      return
    }

    setErro(null)
    setMensagem(null)
    storageService.setGameData(codigo, jogadores)
    storageService.setCurrentPlayer(jogadorSelecionado)

    try {
      setCarregando(true)
      await gameApi.getInitialTickets(codigo, String(jogadorSelecionado.id))
      router.push("/bilhetes-destino")
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        // Este jogador já escolheu bilhetes - vá direto para o jogo
        router.push("/jogo")
        return
      }
      console.error("Erro ao entrar como jogador:", error)
      const mensagemErro =
        error instanceof ApiError
          ? error.message
          : "Não foi possível entrar na partida. Tente novamente."
      setErro(mensagemErro)
    } finally {
      setCarregando(false)
    }
  }, [codigoPartida, jogadores, selectedPlayerId, router])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="bg-white rounded-xl shadow-xl p-8">
          <div className="flex flex-col gap-2 mb-6">
            <h1 className="text-4xl font-bold text-gray-900">Entrar em uma partida</h1>
            <p className="text-gray-600">Use o código gerado na criação da partida ou o link compartilhado.</p>
          </div>

          <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-800 font-semibold">Compartilhe com os amigos</p>
            <p className="text-sm text-blue-700">Link direto: <span className="font-mono">{shareLink || "Digite o código para gerar o link"}</span></p>
            <div className="flex flex-col sm:flex-row gap-2 mt-3">
              <input
                type="text"
                value={codigoPartida}
                onChange={(e) => setCodigoPartida(e.target.value)}
                placeholder="Código da partida"
                className="flex-1 rounded-md border border-blue-200 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <button
                onClick={() => buscarPartida()}
                disabled={carregando}
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-md transition-colors disabled:bg-blue-300"
              >
                {carregando ? "Buscando..." : "Buscar partida"}
              </button>
              <button
                onClick={copiarLink}
                disabled={!shareLink}
                className="bg-white border border-blue-200 text-blue-700 font-semibold px-4 py-2 rounded-md hover:border-blue-400 disabled:opacity-60"
              >
                Copiar link
              </button>
            </div>
          </div>

          {erro && (
            <div className="mb-4 rounded-md bg-red-50 border border-red-200 px-4 py-3 text-red-700">
              {erro}
            </div>
          )}

          {mensagem && (
            <div className="mb-4 rounded-md bg-green-50 border border-green-200 px-4 py-3 text-green-700">
              {mensagem}
            </div>
          )}

          {jogadores.length > 0 && (
            <div className="mb-6">
              <p className="text-lg font-semibold text-gray-800 mb-3">
                Quem é você nesta partida?
              </p>
              <div className="grid sm:grid-cols-2 gap-3">
                {jogadores.map((jogador) => {
                  const selecionado = selectedPlayerId === jogador.id
                  return (
                    <button
                      key={jogador.id}
                      onClick={() => setSelectedPlayerId(String(jogador.id))}
                      className={`text-left rounded-lg border px-4 py-3 transition-colors ${
                        selecionado
                          ? "border-blue-500 bg-blue-50 shadow-sm"
                          : "border-gray-200 hover:border-blue-200"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className="w-10 h-10 rounded-full border border-gray-200"
                          style={{ backgroundColor: jogador.cor?.toLowerCase() || "#e5e7eb" }}
                        />
                        <div>
                          <p className="font-semibold text-gray-900">{jogador.nome}</p>
                          <p className="text-sm text-gray-600">Cor: {jogador.cor}</p>
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={() => router.push("/setup")}
              className="flex-1 px-6 py-3 rounded-md border border-gray-200 text-gray-700 hover:border-gray-400"
            >
              Criar nova partida
            </button>
            <button
              onClick={entrarComoJogador}
              disabled={!selectedPlayerId || !codigoPartida}
              className="flex-1 px-6 py-3 rounded-md bg-blue-600 text-white font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:text-gray-600"
            >
              Entrar na partida
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
