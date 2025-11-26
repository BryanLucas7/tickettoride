/**
 * useGameEnd - Hook para fim de jogo e pontuação
 * 
 * Responsabilidade única: Gerenciar o estado de fim de jogo,
 * carregar pontuação final e navegação pós-jogo.
 */

import { useState, useEffect, useCallback, useRef } from "react"
import { useRouter } from "next/navigation"
import type { GameState, CorJogador } from "@/types/game"
import { asJogadorId } from "@/types/game"
import { gameApi, type PontuacaoApi } from "@/lib/services/gameApi"
import { storageService } from "@/lib/services/storageService"
import { normalizarCorParaUI } from "@/lib/gameRules"
import type { UseGameEndReturn, PontuacaoFinalResumo } from "./types"

interface UseGameEndProps {
  gameState: GameState | null
  limparDadosJogo: () => void
}

export function useGameEnd({ gameState, limparDadosJogo }: UseGameEndProps): UseGameEndReturn {
  const router = useRouter()
  
  const [pontuacaoFinal, setPontuacaoFinal] = useState<PontuacaoFinalResumo[]>([])
  const [mostrarTelaFimJogo, setMostrarTelaFimJogo] = useState(false)
  const [mensagemFimJogo, setMensagemFimJogo] = useState<string | null>(null)
  
  const fimJogoProcessadoRef = useRef(false)
  
  /**
   * Carrega pontuação final do backend
   */
  const carregarPontuacaoFinal = useCallback(async (gameId?: string) => {
    const idParaUso = gameId || storageService.getGameId()
    if (!idParaUso) return

    try {
      const data = await gameApi.getFinalScore(idParaUso)
      const pontuacoesConvertidas: PontuacaoFinalResumo[] = Array.isArray(data.pontuacoes)
        ? data.pontuacoes.map((pontuacao: PontuacaoApi) => ({
            jogadorId: asJogadorId(pontuacao.jogador_id),
            jogadorNome: pontuacao.jogador_nome,
            jogadorCor: normalizarCorParaUI(pontuacao.jogador_cor) as CorJogador,
            pontosRotas: pontuacao.pontos_rotas ?? 0,
            bilhetesCompletos: Array.isArray(pontuacao.bilhetes_completos)
              ? pontuacao.bilhetes_completos.map((bilhete) => ({
                  origem: bilhete.origem ?? bilhete.cidadeOrigem ?? "?",
                  destino: bilhete.destino ?? bilhete.cidadeDestino ?? "?",
                  pontos: bilhete.pontos ?? 0,
                  completo: true
                }))
              : [],
            bilhetesIncompletos: Array.isArray(pontuacao.bilhetes_incompletos)
              ? pontuacao.bilhetes_incompletos.map((bilhete) => ({
                  origem: bilhete.origem ?? bilhete.cidadeOrigem ?? "?",
                  destino: bilhete.destino ?? bilhete.cidadeDestino ?? "?",
                  pontos: bilhete.pontos ?? 0,
                  completo: false
                }))
              : [],
            pontosBilhetesPositivos: pontuacao.pontos_bilhetes_positivos ?? 0,
            pontosBilhetesNegativos: pontuacao.pontos_bilhetes_negativos ?? 0,
            bonusMaiorCaminho: Boolean(pontuacao.bonus_maior_caminho),
            pontosMaiorCaminho:
              pontuacao.pontos_maior_caminho ?? (pontuacao.bonus_maior_caminho ? 10 : 0),
            pontuacaoTotal: pontuacao.pontuacao_total ?? 0,
            tamanhoMaiorCaminho: pontuacao.tamanho_maior_caminho
          }))
        : []

      if (pontuacoesConvertidas.length === 0) {
        setMensagemFimJogo("⚠️ Pontuação final indisponível. Recarregue a página.")
        setMostrarTelaFimJogo(false)
        return
      }

      setPontuacaoFinal(pontuacoesConvertidas)
      setMensagemFimJogo("🏁 Jogo finalizado! Veja o resultado.")
      setMostrarTelaFimJogo(true)
    } catch (error) {
      console.error("Erro ao carregar pontuação final:", error)
      setMensagemFimJogo("⚠️ Não foi possível carregar a pontuação final. Recarregue a página.")
      setMostrarTelaFimJogo(false)
    }
  }, [])
  
  /**
   * Processa fim de jogo automaticamente
   */
  useEffect(() => {
    if (gameState?.finalizado && !fimJogoProcessadoRef.current) {
      fimJogoProcessadoRef.current = true
      carregarPontuacaoFinal(gameState.game_id)
    }
  }, [gameState?.finalizado, gameState?.game_id, carregarPontuacaoFinal])
  
  /**
   * Reset quando gameState muda para novo jogo
   */
  useEffect(() => {
    if (gameState && !gameState.finalizado) {
      fimJogoProcessadoRef.current = false
      setPontuacaoFinal([])
      setMostrarTelaFimJogo(false)
      setMensagemFimJogo(null)
    }
  }, [gameState?.game_id])
  
  /**
   * Volta para o menu principal
   */
  const handleVoltarMenu = useCallback(() => {
    limparDadosJogo()
    router.push("/")
  }, [limparDadosJogo, router])
  
  /**
   * Inicia um novo jogo
   */
  const handleJogarNovamente = useCallback(() => {
    limparDadosJogo()
    router.push("/setup")
  }, [limparDadosJogo, router])
  
  return {
    pontuacaoFinal,
    mostrarTelaFimJogo,
    mensagemFimJogo,
    carregarPontuacaoFinal,
    handleVoltarMenu,
    handleJogarNovamente
  }
}
