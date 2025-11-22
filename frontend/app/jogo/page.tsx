"use client"

import { useState, useEffect, useRef } from "react"
import { useRouter } from "next/navigation"
import MaoCartas from "@/components/MaoCartas"
import Board from "@/components/Board"
import PainelBilhetesDestino from "@/components/PainelBilhetesDestino"
import TelaFimJogo, { PontuacaoFinal as PontuacaoFinalResumo } from "@/components/TelaFimJogo"

// Tipos de interfaces
interface Jogador {
  id: string  // UUID string
  nome: string
  cor: string
  trens_disponiveis: number
  pontos: number
}

interface CartaVagao {
  cor: string
  eh_locomotiva?: boolean
}

interface Rota {
  id: string
  cidadeA: string
  cidadeB: string
  comprimento: number
  cor: string
  proprietario_id: string | null
  proprietario_nome: string | null
  proprietario_cor: string | null
  conquistada: boolean
}

interface BilheteDestino {
  id: string
  cidadeOrigem: string
  cidadeDestino: string
  pontos: number
  index: number
  completo?: boolean  // Adicionado para compatibilidade com o componente
}

interface MaiorCaminhoLeader {
  jogador_id: string
  jogador_nome: string
  jogador_cor: string
}

interface MaiorCaminhoStatus {
  comprimento: number
  lideres: MaiorCaminhoLeader[]
}

interface GameState {
  game_id: string
  iniciado: boolean
  finalizado: boolean
  jogadores: Jogador[]
  jogador_atual_id: string | null
  cartas_visiveis: CartaVagao[]
  maior_caminho?: MaiorCaminhoStatus
}


// Cores disponíveis para o mapa
const CORES: Record<string, string> = {
  VERMELHO: "#EF4444",
  AZUL: "#3B82F6",
  VERDE: "#10B981",
  AMARELO: "#F59E0B",
  PRETO: "#1F2937",
  ROXO: "#8B5CF6",
  BRANCO: "#F3F4F6",
  LARANJA: "#F97316",
  CINZA: "#9CA3AF"
}

const DEFAULT_API_URL = "http://localhost:8000"
const GAME_STORAGE_KEY = "gameId"

const PONTOS_ROTA: Record<number, number> = {
  1: 1,
  2: 2,
  3: 4,
  4: 7,
  5: 10,
  6: 15
}

const MAPA_CORES_FINAIS: Record<string, string> = {
  vermelho: "red",
  azul: "blue",
  verde: "green",
  amarelo: "yellow",
  roxo: "purple",
  laranja: "orange",
  rosa: "pink",
  preto: "black",
  branco: "white",
  cinza: "teal"
}

function resolveApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const envUrl = process.env.NEXT_PUBLIC_API_URL
    if (envUrl && envUrl.length > 0) {
      return envUrl
    }

    if (window.location.hostname.includes("app.github.dev")) {
      const translatedHost = window.location.hostname.replace(/-300[0-9]/, "-8000")
      return `${window.location.protocol}//${translatedHost}`
    }
  } else if (process.env.NEXT_PUBLIC_API_URL && process.env.NEXT_PUBLIC_API_URL.length > 0) {
    return process.env.NEXT_PUBLIC_API_URL
  }

  return DEFAULT_API_URL
}

function apiFetch(path: string, init?: RequestInit) {
  const baseUrl = resolveApiBaseUrl()
  return fetch(`${baseUrl}${path}`, init)
}

export default function JogoPage() {
  const router = useRouter()
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [minhasCartas, setMinhasCartas] = useState<CartaVagao[]>([])
  const [meusBilhetes, setMeusBilhetes] = useState<BilheteDestino[]>([])
  const [rotasDoJogo, setRotasDoJogo] = useState<Rota[]>([])  // Novo estado para rotas
  const [jogadorAtualId, setJogadorAtualId] = useState<string>("0")  // ID do jogador da vez (dinâmico)
  const [mensagem, setMensagem] = useState("")
  const [carregando, setCarregando] = useState(true)
  const [cartasCompradasNesteTurno, setCartasCompradasNesteTurno] = useState(0)
  const [turnoCompraCompleto, setTurnoCompraCompleto] = useState(false)
  const [bloquearLocomotivaAberta, setBloquearLocomotivaAberta] = useState(false)
  const [mensagemCompraCartas, setMensagemCompraCartas] = useState<string | null>(null)
  const [pontuacaoFinal, setPontuacaoFinal] = useState<PontuacaoFinalResumo[]>([])
  const [mostrarTelaFimJogo, setMostrarTelaFimJogo] = useState(false)
  const [mensagemFimJogo, setMensagemFimJogo] = useState<string | null>(null)
  
  // Novos estados para modais
  const [mostrarModalBilhetes, setMostrarModalBilhetes] = useState(false)
  const [bilhetesDisponiveis, setBilhetesDisponiveis] = useState<BilheteDestino[]>([])
  const [cartasSelecionadas, setCartasSelecionadas] = useState<number[]>([])
  const [bilhetesSelecionados, setBilhetesSelecionados] = useState<number[]>([])
  const [fluxoBilhetesAtivo, setFluxoBilhetesAtivo] = useState(false)
  const [carregandoBilhetesPreview, setCarregandoBilhetesPreview] = useState(false)
  const [rotaSelecionada, setRotaSelecionada] = useState<string | null>(null)
  const initialTicketsHandledRef = useRef<Set<string>>(new Set())
  const currentGameIdRef = useRef<string | null>(null)
  const jogadorAtualAnteriorRef = useRef<string | null>(null)
  const fimJogoProcessadoRef = useRef(false)

  useEffect(() => {
    setCartasSelecionadas([])
  }, [rotaSelecionada])

  const rotaSelecionadaInfo = rotaSelecionada
    ? rotasDoJogo.find((rota) => rota.id === rotaSelecionada) ?? null
    : null

  const normalizarCorFimJogo = (cor?: string | null) => {
    if (!cor) return "blue"
    const chave = cor.toLowerCase()
    return MAPA_CORES_FINAIS[chave] || chave || "blue"
  }

  // Função auxiliar para limpar localStorage
  const limparDadosJogo = () => {
    localStorage.removeItem(GAME_STORAGE_KEY)
    localStorage.removeItem("current_game_id")
    initialTicketsHandledRef.current = new Set()
    currentGameIdRef.current = null
    fimJogoProcessadoRef.current = false
    setPontuacaoFinal([])
    setMostrarTelaFimJogo(false)
    setMensagemFimJogo(null)
  }

  // Busca o estado do jogo
  useEffect(() => {
    const storedGameId = localStorage.getItem(GAME_STORAGE_KEY)

    if (!storedGameId) {
      setMensagem("Nenhum jogo ativo. Crie um jogo na tela de configuração.")
      setCarregando(false)
      router.push("/setup")
      return
    }

    buscarEstadoJogo(storedGameId)

    const interval = setInterval(() => {
      const currentGameId = localStorage.getItem(GAME_STORAGE_KEY)
      if (currentGameId) {
        buscarEstadoJogo(currentGameId)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [router])

  const buscarEstadoJogo = async (gameId: string) => {
    try {
      if (currentGameIdRef.current !== gameId) {
        currentGameIdRef.current = gameId
        initialTicketsHandledRef.current = new Set()
        fimJogoProcessadoRef.current = false
        setPontuacaoFinal([])
        setMostrarTelaFimJogo(false)
        setMensagemFimJogo(null)
      }

      const response = await apiFetch(`/games/${gameId}`)
      if (!response.ok) {
        if (response.status === 404) {
          console.warn("Jogo não encontrado (404). Redirecionando para o setup.")
          limparDadosJogo()
          setMensagem("Jogo anterior não está mais disponível. Crie um novo jogo.")
          setCarregando(false)
          router.push("/setup")
          return
        }

        throw new Error(`Erro ao buscar jogo: ${response.status}`)
      }

      const state = await response.json()
      setGameState(state)

      const jogadorAtualStateId = state.jogador_atual_id || null
      const jogadorAnterior = jogadorAtualAnteriorRef.current

      if (jogadorAtualStateId && jogadorAtualStateId !== jogadorAnterior) {
        setCartasCompradasNesteTurno(0)
        setTurnoCompraCompleto(false)
        setBloquearLocomotivaAberta(false)
        setMensagemCompraCartas(null)
      }

      jogadorAtualAnteriorRef.current = jogadorAtualStateId

      if (jogadorAtualStateId) {
        setJogadorAtualId(jogadorAtualStateId)
      }

      if (state.jogador_atual_id) {
        const cartasResponse = await apiFetch(
          `/games/${gameId}/players/${state.jogador_atual_id}/cards`
        )
        if (cartasResponse.ok) {
          const cartasData = await cartasResponse.json()
          if (cartasData.cards && Array.isArray(cartasData.cards)) {
            setMinhasCartas(cartasData.cards)
          } else {
            console.warn("Formato de cartas inválido, limpando dados...")
            limparDadosJogo()
            setMensagem("Dados do jogo corrompidos. Crie um novo jogo.")
            setCarregando(false)
            router.push("/setup")
            return
          }
        } else if (cartasResponse.status === 404) {
          setMinhasCartas([])
        }
      } else {
        setMinhasCartas([])
      }

      if (jogadorAtualStateId) {
        const bilhetesResponse = await apiFetch(
          `/games/${gameId}/players/${jogadorAtualStateId}/tickets`
        )

        if (bilhetesResponse.ok) {
          const bilhetesData = await bilhetesResponse.json()
          if (bilhetesData.tickets && Array.isArray(bilhetesData.tickets)) {
            setMeusBilhetes(bilhetesData.tickets)
          }
        } else if (bilhetesResponse.status === 404) {
          setMeusBilhetes([])
        }
      }

      // Verifica se há bilhetes iniciais pendentes de escolha apenas uma vez por jogador
      const jogadorAtual = state.jogador_atual_id
      if (jogadorAtual && !initialTicketsHandledRef.current.has(jogadorAtual)) {
        const bilhetesIniciaisResponse = await apiFetch(
          `/games/${gameId}/players/${jogadorAtual}/tickets/initial`
        )

        if (bilhetesIniciaisResponse.ok) {
          const bilhetesIniciaisData = await bilhetesIniciaisResponse.json()
          if (bilhetesIniciaisData.bilhetes && bilhetesIniciaisData.bilhetes.length > 0) {
            // Escolhe automaticamente todos os bilhetes iniciais (ou você pode criar um modal)
            const todosIds = bilhetesIniciaisData.bilhetes.map((b: any) => b.id)
            await apiFetch(
              `/games/${gameId}/players/${jogadorAtual}/tickets/initial`,
              {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ bilhetes_escolhidos: todosIds })
              }
            )
            // Atualiza bilhetes após escolha
            const novaBuscaBilhetes = await apiFetch(
              `/games/${gameId}/players/${jogadorAtual}/tickets`
            )
            if (novaBuscaBilhetes.ok) {
              const novosBilhetesData = await novaBuscaBilhetes.json()
              if (novosBilhetesData.tickets && Array.isArray(novosBilhetesData.tickets)) {
                setMeusBilhetes(novosBilhetesData.tickets)
              }
            }
          }
          initialTicketsHandledRef.current.add(jogadorAtual)
        } else if (bilhetesIniciaisResponse.status === 404) {
          initialTicketsHandledRef.current.add(jogadorAtual)
        } else {
          console.warn("Falha ao consultar bilhetes iniciais:", bilhetesIniciaisResponse.status)
        }
      }

      // Busca rotas do jogo (com informações de proprietário)
      const rotasResponse = await apiFetch(`/games/${gameId}/routes`)
      if (rotasResponse.ok) {
        const rotasData = await rotasResponse.json()
        if (rotasData.routes && Array.isArray(rotasData.routes)) {
          setRotasDoJogo(rotasData.routes)
        }
      }

      // Atualiza mensagem com o nome do jogador da vez
      if (state.finalizado) {
        setMensagem("🏁 Jogo finalizado! Aguarde os resultados finais.")
      } else {
        const jogadorDaVez = state.jogadores.find((j: Jogador) => j.id === state.jogador_atual_id)
        setMensagem(
          jogadorDaVez 
            ? `🎮 Vez de: ${jogadorDaVez.nome}` 
            : "🎮 Aguardando..."
        )
      }
      setCarregando(false)
    } catch (error) {
      console.error("Erro ao buscar jogo:", error)
      // Se for erro de rede/conexão, limpa dados antigos
      limparDadosJogo()
      setMensagem("❌ Erro ao conectar com o servidor. Dados locais limpos, recarregue a página.")
      setCarregando(false)
      router.push("/setup")
    }
  }

  const carregarPontuacaoFinal = async (gameId?: string) => {
    const idParaUso = gameId || localStorage.getItem(GAME_STORAGE_KEY)
    if (!idParaUso) {
      return
    }

    try {
      const response = await apiFetch(`/games/${idParaUso}/pontuacao-final`)
      if (!response.ok) {
        console.warn("Falha ao carregar pontuação final:", await response.text())
        setMensagemFimJogo("⚠️ Não foi possível carregar a pontuação final. Tente novamente.")
        setMostrarTelaFimJogo(false)
        return
      }

      const data = await response.json()
      const pontuacoesConvertidas: PontuacaoFinalResumo[] = Array.isArray(data.pontuacoes)
        ? data.pontuacoes.map((pontuacao: any) => ({
            jogadorId: pontuacao.jogador_id,
            jogadorNome: pontuacao.jogador_nome,
            jogadorCor: normalizarCorFimJogo(pontuacao.jogador_cor),
            pontosRotas: pontuacao.pontos_rotas ?? 0,
            bilhetesCompletos: Array.isArray(pontuacao.bilhetes_completos)
              ? pontuacao.bilhetes_completos.map((bilhete: any) => ({
                  origem: bilhete.origem ?? bilhete.cidadeOrigem ?? "?",
                  destino: bilhete.destino ?? bilhete.cidadeDestino ?? "?",
                  pontos: bilhete.pontos ?? 0,
                  completo: true
                }))
              : [],
            bilhetesIncompletos: Array.isArray(pontuacao.bilhetes_incompletos)
              ? pontuacao.bilhetes_incompletos.map((bilhete: any) => ({
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
      setMensagemFimJogo(data.mensagem ?? "🏁 Jogo finalizado! Veja o resultado.")
      setMostrarTelaFimJogo(true)
    } catch (error) {
      console.error("Erro ao carregar pontuação final:", error)
      setMensagemFimJogo("⚠️ Não foi possível carregar a pontuação final. Recarregue a página.")
      setMostrarTelaFimJogo(false)
    }
  }

  useEffect(() => {
    if (gameState?.finalizado && !fimJogoProcessadoRef.current) {
      fimJogoProcessadoRef.current = true
      carregarPontuacaoFinal(gameState.game_id)
    }
  }, [gameState?.finalizado, gameState?.game_id])

  const handleVoltarMenu = () => {
    limparDadosJogo()
    router.push("/")
  }

  const handleJogarNovamente = () => {
    limparDadosJogo()
    router.push("/setup")
  }

  // Ações do jogo
  const comprarCartaFechada = async () => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview) {
      setMensagem("⚠️ Conclua a escolha de bilhetes antes de realizar outra ação.")
      return
    }

    const gameId = localStorage.getItem(GAME_STORAGE_KEY)
    if (!gameId) return

    try {
      const response = await apiFetch(
        `/games/${gameId}/players/${jogadorAtualId}/draw-closed`,
        { method: "POST" }
      )
      
      if (response.ok) {
        const data = await response.json()
        const cartaComprada = data.card || {}
        const ehLocomotivaFechada = cartaComprada.eh_locomotiva === true
        const turnoFinalizado = data.turn_completed === true

        setMensagem(`✅ ${data.message}`)

        setCartasCompradasNesteTurno((prev) => {
          if (turnoFinalizado) {
            return 0
          }
          return prev + 1
        })

        setTurnoCompraCompleto(turnoFinalizado)

        if (turnoFinalizado) {
          setBloquearLocomotivaAberta(true)
          setMensagemCompraCartas("Turno de compra concluído. Aguarde o próximo movimento.")
        } else {
          setBloquearLocomotivaAberta(true)
          setMensagemCompraCartas(
            ehLocomotivaFechada
              ? "Locomotiva comprada do baralho fechado continua permitindo uma segunda carta. Locomotivas visíveis permanecem bloqueadas."
              : "Você já comprou uma carta. Locomotivas visíveis ficam bloqueadas, mas é permitido pegar outra carta fechada ou uma aberta que não seja locomotiva."
          )
        }

        await buscarEstadoJogo(gameId)

        if (turnoFinalizado) {
          setTimeout(() => {
            setMensagem(`🔄 Turno completo! Vez do jogador ${data.next_player}`)
            setTimeout(async () => {
              await buscarEstadoJogo(gameId)
            }, 2000)
          }, 1500)
        }
      } else {
        const error = await response.json()
        const detalhe = error.detail || "Não foi possível comprar carta fechada."
        setMensagem(`❌ ${detalhe}`)
        setMensagemCompraCartas(detalhe)
      }
    } catch (error) {
      setMensagem("❌ Erro ao comprar carta")
      setMensagemCompraCartas("Não foi possível comprar carta. Verifique sua conexão e tente novamente.")
    }
  }

  const comprarCartaAberta = async (index: number) => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview) {
      setMensagem("⚠️ Finalize a seleção de bilhetes para seguir com outras ações.")
      return
    }

    const gameId = localStorage.getItem(GAME_STORAGE_KEY)
    if (!gameId || turnoCompraCompleto) {
      return
    }

    const cartaSelecionada = gameState?.cartas_visiveis?.[index]
    const ehLocomotivaSelecionada = cartaSelecionada
      ? cartaSelecionada.eh_locomotiva === true || cartaSelecionada.cor?.toLowerCase() === "locomotiva"
      : false

    if (bloquearLocomotivaAberta && ehLocomotivaSelecionada) {
      setMensagemCompraCartas("Locomotivas visíveis estão bloqueadas porque você já comprou uma carta neste turno.")
      return
    }

    if (!cartaSelecionada) {
      setMensagemCompraCartas("Carta indisponível. Aguarde atualização das cartas visíveis.")
      return
    }

    try {
      const response = await apiFetch(
        `/games/${gameId}/players/${jogadorAtualId}/draw-open/${index}`,
        { method: "POST" }
      )
      
      if (response.ok) {
        const data = await response.json()
        const cartaComprada = data.card || {}
        const ehLocomotivaAberta = cartaComprada.eh_locomotiva === true
        const turnoFinalizado = ehLocomotivaAberta || data.turn_completed === true

        setMensagem(`✅ ${data.message}`)

        setCartasCompradasNesteTurno((prev) => {
          if (turnoFinalizado) {
            return 0
          }
          return prev + 1
        })

        setTurnoCompraCompleto(turnoFinalizado)

        if (ehLocomotivaAberta) {
          setBloquearLocomotivaAberta(true)
          setMensagemCompraCartas("Locomotiva visível comprada: essa escolha encerra sua ação de compra de cartas neste turno.")
        } else if (turnoFinalizado) {
          setBloquearLocomotivaAberta(true)
          setMensagemCompraCartas("Turno de compra concluído. Aguarde o próximo jogador.")
        } else {
          setBloquearLocomotivaAberta(true)
          setMensagemCompraCartas("Você já comprou 1 carta. Locomotivas visíveis ficam bloqueadas até o final do turno.")
        }

        await buscarEstadoJogo(gameId)

        if (turnoFinalizado) {
          setTimeout(() => {
            setMensagem(`🔄 Turno completo! Vez do jogador ${data.next_player}`)
            setTimeout(async () => {
              await buscarEstadoJogo(gameId)
            }, 2000)
          }, 1500)
        }
      } else {
        const error = await response.json()
        const detalhe = error.detail || "Não foi possível comprar esta carta."
        setMensagem(`❌ ${detalhe}`)
        setMensagemCompraCartas(detalhe)
      }
    } catch (error) {
      setMensagem("❌ Erro ao comprar carta")
      setMensagemCompraCartas("Não foi possível comprar carta. Verifique sua conexão e tente novamente.")
    }
  }

  const getCoresBg = (cor: string) => {
    const cores: Record<string, string> = {
      vermelho: "bg-red-500",
      azul: "bg-blue-500",
      verde: "bg-green-500",
      amarelo: "bg-yellow-500",
      preto: "bg-gray-800",
      laranja: "bg-orange-500",
      branco: "bg-white border-4 border-gray-800 shadow-lg",
      roxo: "bg-purple-500",
      locomotiva: "bg-purple-700",
    }
    return cores[cor.toLowerCase()] || "bg-gray-500"
  }

  const getLetraCor = (cor: string): string => {
    const letras: Record<string, string> = {
      vermelho: "V",
      azul: "A",
      verde: "Ve",
      amarelo: "Am",
      laranja: "L",
      preto: "P",
      branco: "B",
      roxo: "R",
      locomotiva: "🚂"
    }
    return letras[cor.toLowerCase()] || cor.charAt(0).toUpperCase()
  }
  
  const getCorTexto = (cor: string): string => {
    // Cartas brancas usam texto preto
    if (cor.toLowerCase() === "branco") {
      return "text-gray-900"
    }
    return "text-white"
  }

  const toggleCartaSelecionada = (indice: number, limite?: number) => {
    setCartasSelecionadas((selecionadas) => {
      if (selecionadas.includes(indice)) {
        return selecionadas.filter((valor) => valor !== indice)
      }

      const limiteMaximo = typeof limite === "number" ? limite : rotaSelecionadaInfo?.comprimento

      if (typeof limiteMaximo === "number" && selecionadas.length >= limiteMaximo) {
        return selecionadas
      }

      return [...selecionadas, indice]
    })
  }

  const handleSelecaoRotaMapa = (rotaId: string | null) => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview || acaoCartasBloqueiaOutras) {
      setMensagem(
        acaoCartasBloqueiaOutras
          ? "⚠️ Conclua a compra de cartas antes de selecionar rotas."
          : "⚠️ Termine a compra de bilhetes antes de selecionar rotas."
      )
      return
    }

    if (!rotaId) {
      setRotaSelecionada(null)
      return
    }

    const rotaInfo = rotasDoJogo.find((rota) => rota.id === rotaId)

    if (rotaInfo?.conquistada) {
      setMensagem("⚠️ Essa rota já foi conquistada por outro jogador.")
      setRotaSelecionada(null)
      return
    }

    setRotaSelecionada(rotaId)
  }

  const conquistarRota = async () => {
    if (fluxoBilhetesAtivo || carregandoBilhetesPreview || acaoCartasBloqueiaOutras) {
      setMensagem(
        acaoCartasBloqueiaOutras
          ? "⚠️ Você escolheu comprar cartas neste turno. Finalize essa ação antes de conquistar rotas."
          : "⚠️ Termine a compra de bilhetes antes de conquistar rotas."
      )
      return
    }

    if (!rotaSelecionada) {
      setMensagem("❌ Selecione uma rota disponível no mapa antes de conquistar")
      return
    }

    if (cartasSelecionadas.length === 0) {
      setMensagem("❌ Escolha as cartas que serão usadas na conquista da rota")
      return
    }

    if (!rotaSelecionadaInfo) {
      setMensagem("❌ Rota selecionada não encontrada. Atualize o estado do jogo.")
      return
    }
    if (rotaSelecionadaInfo.conquistada) {
      setMensagem("❌ Essa rota já foi conquistada.")
      return
    }

    if (cartasSelecionadas.length !== rotaSelecionadaInfo.comprimento) {
      setMensagem(`❌ Selecione ${rotaSelecionadaInfo.comprimento} carta${rotaSelecionadaInfo.comprimento > 1 ? "s" : ""} para conquistar esta rota.`)
      return
    }

    const cartasSelecionadasDetalhes = cartasSelecionadas
      .map((indice) => minhasCartas[indice])
      .filter((carta): carta is CartaVagao => Boolean(carta))

    if (rotaSelecionadaInfo.cor.toLowerCase() === "cinza") {
      const coresNaoLocomotiva = new Set(
        cartasSelecionadasDetalhes
          .filter((carta) => !carta.eh_locomotiva)
          .map((carta) => carta.cor.toLowerCase())
      )

      if (coresNaoLocomotiva.size > 1) {
        setMensagem("❌ Rotas cinza exigem todas as cartas da mesma cor. Use locomotivas como coringa para completar a sequência.")
        return
      }

      if (coresNaoLocomotiva.size === 0 && cartasSelecionadasDetalhes.length > 0 && cartasSelecionadasDetalhes.every((carta) => carta.eh_locomotiva !== true)) {
        setMensagem("❌ Escolha cartas da mesma cor ou locomotivas para conquistar esta rota cinza.")
        return
      }
    }

    const cartasParaEnviar = cartasSelecionadasDetalhes
      .map((carta) => carta.cor)
      .filter((cor): cor is string => typeof cor === "string")
      .map((cor) => cor.toLowerCase())

    if (cartasParaEnviar.length !== cartasSelecionadas.length) {
      setMensagem("❌ Não foi possível localizar todas as cartas selecionadas. Atualize as cartas e tente novamente.")
      return
    }

    try {
      const gameId = localStorage.getItem(GAME_STORAGE_KEY)
      const response = await apiFetch(
        `/games/${gameId}/players/${jogadorAtualId}/conquer-route`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            player_id: jogadorAtualId,
            rota_id: rotaSelecionada,
            cartas_usadas: cartasParaEnviar
          })
        }
      )

      const data = await response.json()

      if (response.ok && data.success) {
        setMensagem(`✅ ${data.message} (+${data.points} pontos)`)
        setRotaSelecionada(null)
        setCartasSelecionadas([])
        
        // Atualiza estado primeiro
        await buscarEstadoJogo(gameId)
        
        // Notificar turno passado automaticamente
        setTimeout(() => {
          setMensagem(`🔄 Turno completo! Vez do jogador ${data.next_player}`)
          // Após 2 segundos, volta para mensagem padrão
          setTimeout(async () => {
            await buscarEstadoJogo(gameId)
          }, 2000)
        }, 2000)
      } else {
        const detalhes = Array.isArray(data.detail)
          ? data.detail.map((item: any) => item.msg || JSON.stringify(item)).join(" | ")
          : data.detail
        console.error("Falha ao conquistar rota", { payload: { rota_id: rotaSelecionada, cartas_usadas: cartasParaEnviar }, resposta: data })
        setMensagem(`❌ ${detalhes || data.message || "Não foi possível conquistar a rota"}`)
      }
    } catch (error) {
      setMensagem("❌ Erro ao conquistar rota")
    }
  }

  // ========== NOVAS FUNÇÕES: COMPRA DE BILHETES ==========
  const abrirModalBilhetes = async () => {
    const gameId = localStorage.getItem(GAME_STORAGE_KEY)

    if (!gameId) {
      setMensagem("❌ Jogo não encontrado. Recarregue a página.")
      return
    }

    if (turnoCompraCompleto) {
      setMensagem("⚠️ Você já realizou a ação deste turno.")
      return
    }

    if (cartasCompradasNesteTurno > 0 && !turnoCompraCompleto) {
      setMensagem("⚠️ Você já começou a comprar cartas. Finalize a segunda compra antes de pegar bilhetes.")
      return
    }

    if (fluxoBilhetesAtivo || carregandoBilhetesPreview) {
      setMensagem("⚠️ Finalize a compra de bilhetes já iniciada antes de ver novas cartas.")
      return
    }

    setCarregandoBilhetesPreview(true)
    setMensagem("🔎 Buscando novas opções de bilhetes de destino...")

    try {
      const response = await apiFetch(
        `/games/${gameId}/players/${jogadorAtualId}/tickets/preview`,
        { method: "POST" }
      )

      if (!response.ok) {
        const error = await response.json()
        setMensagem(`❌ ${error.detail || "Não foi possível obter bilhetes"}`)
        return
      }

      const data = await response.json()
      const bilhetes = Array.isArray(data.tickets) ? data.tickets : []

      if (bilhetes.length === 0) {
        setMensagem("⚠️ Nenhum bilhete disponível no momento.")
        setMostrarModalBilhetes(false)
        setFluxoBilhetesAtivo(false)
        return
      }

      setBilhetesDisponiveis(
        bilhetes.map((bilhete: any, idx: number) => ({
          id: bilhete.id,
          cidadeOrigem: bilhete.origem ?? bilhete.cidadeOrigem,
          cidadeDestino: bilhete.destino ?? bilhete.cidadeDestino,
          pontos: bilhete.pontos,
          index: typeof bilhete.index === "number" ? bilhete.index : idx
        }))
      )
      setBilhetesSelecionados([])
      setMostrarModalBilhetes(true)
      setFluxoBilhetesAtivo(true)
      setMensagem("✍️ Escolha pelo menos 1 bilhete para concluir sua ação deste turno.")
    } catch (error) {
      console.error("Erro ao obter bilhetes:", error)
      setMensagem("❌ Erro ao obter bilhetes")
    } finally {
      setCarregandoBilhetesPreview(false)
    }
  }

  const comprarBilhetes = async () => {
    if (bilhetesSelecionados.length === 0) {
      setMensagem("❌ Escolha pelo menos 1 bilhete")
      return
    }

    try {
      const gameId = localStorage.getItem(GAME_STORAGE_KEY)
      if (!gameId) {
        setMensagem("❌ Jogo não encontrado. Recarregue a página.")
        return
      }

      const response = await apiFetch(
        `/games/${gameId}/players/${jogadorAtualId}/buy-tickets`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            bilhetes_escolhidos: bilhetesSelecionados.map(String) // Índices como strings
          })
        }
      )

      const data = await response.json()

      if (response.ok && data.success) {
        setMensagem(`✅ ${data.message}`)
        setMostrarModalBilhetes(false)
        setFluxoBilhetesAtivo(false)
        setBilhetesDisponiveis([])
        setBilhetesSelecionados([])
        
        // Atualiza estado primeiro
        await buscarEstadoJogo(gameId!)
        
        // Notificar turno passado automaticamente
        setTimeout(() => {
          setMensagem(`🔄 Turno completo! Vez do jogador ${data.next_player}`)
          // Após 2 segundos, volta para mensagem padrão
          setTimeout(async () => {
            await buscarEstadoJogo(gameId!)
          }, 2000)
        }, 2000)
      } else {
        setMensagem(`❌ ${data.detail || data.message}`)
      }
    } catch (error) {
      setMensagem("❌ Erro ao comprar bilhetes")
    }
  }

  if (carregando) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-700">Carregando jogo...</p>
        </div>
      </div>
    )
  }

  if (!gameState) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="bg-white rounded-lg shadow-xl p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Erro</h2>
          <p className="text-gray-700 mb-4">{mensagem}</p>
          <button
            onClick={() => router.push("/")}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg"
          >
            Voltar ao Início
          </button>
        </div>
      </div>
    )
  }

  // Encontra o jogador atual pelo ID (agora é string)
  const jogadorAtual = gameState.jogadores.find(j => j.id === jogadorAtualId)
  const bilhetesAtuais = meusBilhetes
  const ehMinhaVez = true  // Sempre true pois a tela sempre mostra o jogador da vez
  const cartasCompradasNoTurno = turnoCompraCompleto ? 2 : cartasCompradasNesteTurno
  const fluxoCompraCartasAtivo = cartasCompradasNesteTurno > 0 && !turnoCompraCompleto
  const acaoCartasBloqueiaOutras = fluxoCompraCartasAtivo || turnoCompraCompleto
  const rotasConquistadas = rotasDoJogo
    .filter((rota) => rota.proprietario_id === jogadorAtualId)
    .map((rota) => ({
      id: rota.id,
      origem: rota.cidadeA,
      destino: rota.cidadeB,
      comprimento: rota.comprimento,
      pontos: PONTOS_ROTA[rota.comprimento] || 0
    }))
  const totalPontosRotas = rotasConquistadas.reduce((acc, rota) => acc + rota.pontos, 0)
  const mensagemPrincipal = gameState.finalizado
    ? mensagemFimJogo || "🏁 Jogo finalizado! Veja o resultado final."
    : mensagem

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-4">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-xl p-4 mb-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">🎫 Ticket to Ride - Brasil</h1>
            <button
              onClick={() => router.push("/")}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              Sair
            </button>
          </div>

          {/* Mensagem de status */}
          <div
            className={`mt-4 border-l-4 p-4 rounded ${
              ehMinhaVez
                ? "bg-green-50 border-green-500"
                : "bg-blue-50 border-blue-500"
            }`}
          >
            <p className="text-lg font-semibold">{mensagemPrincipal}</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-4">
          {/* Coluna esquerda - Jogadores */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-lg p-4">
              <h2 className="text-xl font-bold mb-4 text-gray-900">Jogadores</h2>
              <div className="space-y-3">
                {gameState.jogadores.map((jogador) => (
                  <div
                    key={jogador.id}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      jogador.id === gameState.jogador_atual_id
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-200 bg-gray-50"
                    } ${jogador.id === jogadorAtualId ? "ring-2 ring-green-400" : ""}`}
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <div className={`w-10 h-10 rounded-full ${getCoresBg(jogador.cor)}`}></div>
                      <div className="flex-1">
                        <h3 className="font-bold text-gray-900">
                          {jogador.nome}
                          {jogador.id === jogadorAtualId && (
                            <span className="ml-2 text-xs bg-green-600 text-white px-2 py-1 rounded-full">
                              JOGANDO
                            </span>
                          )}
                        </h3>
                        <p className="text-xs text-gray-500 uppercase">{jogador.cor}</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <span className="text-gray-600">Pontuação:</span>
                        <span className="ml-2 font-bold text-lg">{jogador.pontos}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Vagões:</span>
                        <span className="ml-2 font-semibold">{jogador.trens_disponiveis}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Widget dinâmico de Maior Caminho */}
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
                  <p className="text-4xl font-extrabold text-purple-900">{gameState?.maior_caminho?.comprimento ?? 0}</p>
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
                      const corNormalizada = lider.jogador_cor ? lider.jogador_cor.toLowerCase() : ""
                      const corFundo = MAPA_CORES_FINAIS[corNormalizada] || corNormalizada || "#7c3aed"
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

            {/* Ações do turno */}
            {ehMinhaVez && (
              <div className="bg-white rounded-lg shadow-lg p-4">
                <h2 className="text-xl font-bold mb-4 text-gray-900">Ações</h2>
                <div className="space-y-3">
                  {/* Comprar Cartas */}
                  <div className="border-2 border-green-200 rounded-lg p-3">
                    <h3 className="font-semibold text-green-700 mb-2">🃏 Comprar Cartas</h3>
                    
                    {/* Botão para comprar carta aberta */}
                    {gameState?.cartas_visiveis && gameState.cartas_visiveis.length > 0 && (
                      <div className="mb-3">
                        <p className="text-xs text-gray-600 mb-2">Escolha uma carta visível:</p>
                        <div className="flex gap-2 flex-wrap">
                          {gameState.cartas_visiveis.map((carta, index) => {
                            const corNormalizada = carta.cor.toLowerCase()
                            const ehLocomotiva = carta.eh_locomotiva === true || corNormalizada === "locomotiva"
                            const desabilitada =
                              turnoCompraCompleto ||
                              fluxoBilhetesAtivo ||
                              carregandoBilhetesPreview ||
                              (bloquearLocomotivaAberta && ehLocomotiva)
                            const titulo = fluxoBilhetesAtivo
                              ? "Finalize a escolha de bilhetes antes de comprar cartas."
                              : carregandoBilhetesPreview
                                ? "Aguarde o carregamento dos bilhetes."
                                : turnoCompraCompleto
                                  ? "Você já concluiu as compras de cartas deste turno."
                                  : ehLocomotiva && bloquearLocomotivaAberta
                                    ? "Locomotiva visível bloqueada após já ter comprado uma carta."
                                    : `Comprar carta ${carta.cor}`

                            return (
                              <button
                                key={index}
                                type="button"
                                onClick={() => comprarCartaAberta(index)}
                                disabled={desabilitada}
                                className={`relative w-16 h-20 rounded-lg flex items-center justify-center text-xs font-bold transition-all ${
                                  getCoresBg(carta.cor)
                                } ${getCorTexto(carta.cor)} shadow-md hover:scale-105 hover:ring-2 hover:ring-green-400 disabled:hover:scale-100 disabled:hover:ring-0 disabled:cursor-not-allowed disabled:opacity-40 ${
                                  bloquearLocomotivaAberta && ehLocomotiva ? "ring-2 ring-amber-400 ring-offset-2 ring-offset-white" : ""
                                }`}
                                title={titulo}
                              >
                                {getLetraCor(carta.cor)}
                                {bloquearLocomotivaAberta && ehLocomotiva && !turnoCompraCompleto && (
                                  <span className="absolute -top-1 -right-1 bg-amber-100 text-amber-700 text-[10px] font-semibold px-1 py-[1px] rounded-full border border-amber-300">
                                    ⚠️
                                  </span>
                                )}
                              </button>
                            )
                          })}
                        </div>
                      </div>
                    )}
                    
                    {/* Carta Fechada */}
                    <button
                      type="button"
                      className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors text-sm disabled:bg-gray-300 disabled:text-gray-600 disabled:cursor-not-allowed"
                      onClick={comprarCartaFechada}
                      disabled={turnoCompraCompleto || fluxoBilhetesAtivo || carregandoBilhetesPreview}
                      title={
                        fluxoBilhetesAtivo
                          ? "Finalize a escolha de bilhetes antes de comprar cartas."
                          : turnoCompraCompleto
                            ? "Você já concluiu as compras de cartas deste turno."
                            : "Comprar carta do baralho fechado"
                      }
                    >
                      🂠 Comprar do Baralho (Fechada)
                    </button>

                    <p className="text-xs text-gray-500 mt-2">
                      Cartas compradas neste turno: {cartasCompradasNoTurno}/2
                    </p>

                    {mensagemCompraCartas && (
                      <div className="mt-3 flex items-start gap-2 rounded-md border border-amber-200 bg-amber-50 p-2 text-xs text-amber-800">
                        <span className="text-base leading-none">⚠️</span>
                        <span>{mensagemCompraCartas}</span>
                      </div>
                    )}
                  </div>

                  <div className="border-2 border-purple-200 rounded-lg p-3">
                    <h3 className="font-semibold text-purple-700 mb-2">🛤️ Conquistar Rota</h3>
                    <p className="text-sm text-gray-600">
                      Selecione uma rota no mapa e use a seção <strong>Rota selecionada</strong> abaixo para escolher as cartas e confirmar a conquista.
                    </p>
                    <p className="text-xs text-gray-500 mt-2">
                      {rotaSelecionada
                        ? "Rota aguardando confirmação no painel inferior."
                        : "Nenhuma rota selecionada no momento."}
                    </p>
                    {acaoCartasBloqueiaOutras && (
                      <p className="text-xs text-orange-700 mt-2">
                        Você optou por comprar cartas neste turno. Conclua essa ação (segunda compra ou aguarde o próximo turno) para liberar a conquista de rotas.
                      </p>
                    )}
                  </div>
                  <button
                    className="w-full bg-orange-600 hover:bg-orange-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:bg-gray-300 disabled:text-gray-600 disabled:cursor-not-allowed"
                    onClick={abrirModalBilhetes}
                    disabled={
                      fluxoBilhetesAtivo ||
                      carregandoBilhetesPreview ||
                      turnoCompraCompleto ||
                      fluxoCompraCartasAtivo
                    }
                    title={
                      fluxoBilhetesAtivo
                        ? "Finalize a escolha de bilhetes já iniciada."
                        : carregandoBilhetesPreview
                          ? "Carregando cartas de bilhete do baralho..."
                          : fluxoCompraCartasAtivo
                            ? "Você já escolheu comprar cartas neste turno. Termine essa ação primeiro."
                            : turnoCompraCompleto
                              ? "Você já realizou uma ação neste turno. Aguarde o próximo."
                              : "Comprar novos bilhetes de destino"
                    }
                  >
                    {carregandoBilhetesPreview ? "Carregando bilhetes..." : "🎫 Pegar Bilhetes Destino"}
                  </button>

                  {fluxoBilhetesAtivo && (
                    <p className="text-xs text-orange-700 mt-2">
                      Esta ação precisa ser concluída: escolha pelo menos um bilhete para encerrar o turno.
                    </p>
                  )}

                  {mostrarModalBilhetes && (
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
                        {bilhetesDisponiveis.map((bilhete) => {
                          const selecionado = bilhetesSelecionados.includes(bilhete.index)
                          return (
                            <button
                              key={bilhete.index}
                              type="button"
                              onClick={() => {
                                const ticketIndex = bilhete.index
                                setBilhetesSelecionados((selecionadosAtuais) => {
                                  if (selecionadosAtuais.includes(ticketIndex)) {
                                    return selecionadosAtuais.filter((i) => i !== ticketIndex)
                                  }

                                  if (selecionadosAtuais.length >= 3) {
                                    setMensagem("⚠️ Você pode manter no máximo 3 bilhetes.")
                                    return selecionadosAtuais
                                  }

                                  return [...selecionadosAtuais, ticketIndex]
                                })
                              }}
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
                        Selecionados: {bilhetesSelecionados.length}/3
                      </p>

                      <button
                        type="button"
                        onClick={comprarBilhetes}
                        disabled={bilhetesSelecionados.length === 0}
                        className="w-full bg-orange-600 hover:bg-orange-700 disabled:bg-gray-300 disabled:text-gray-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                      >
                        Confirmar escolha ({bilhetesSelecionados.length})
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Coluna central - Mapa */}
          <div className="lg:col-span-2">
            <Board
              rotasDoJogo={rotasDoJogo}
              rotaSelecionadaId={rotaSelecionada}
              onRotaSelecionada={handleSelecaoRotaMapa}
              renderRotaDetalhes={({ rotaMapa, rotaDoJogo }) => {
                if (rotaDoJogo?.conquistada) {
                  return (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-sm text-green-800">
                      Essa rota já foi conquistada por {rotaDoJogo.proprietario_nome}.
                    </div>
                  )
                }

                if (fluxoBilhetesAtivo || carregandoBilhetesPreview || acaoCartasBloqueiaOutras) {
                  return (
                    <p className="text-sm text-orange-700 text-center">
                      {acaoCartasBloqueiaOutras
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

                if (minhasCartas.length === 0) {
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
                        {rotaEhCinza ? "da mesma cor à sua escolha" : `na cor ${corRota.toLowerCase()}` }.
                      </p>
                      <p className="text-xs text-purple-600 mt-1">
                        Cartas locomotiva podem substituir qualquer cor{rotaEhCinza ? ", mas cores diferentes não podem ser misturadas." : "."}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-gray-600 mb-2">Clique nas cartas para selecioná-las:</p>
                      <div className="flex flex-wrap gap-2">
                        {minhasCartas.map((carta, idx) => {
                          const selecionada = cartasSelecionadas.includes(idx)
                          return (
                            <button
                              key={`rota-card-${idx}-${carta.cor}`}
                              type="button"
                              onClick={() => toggleCartaSelecionada(idx, cartasNecessarias)}
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
                        Cartas selecionadas: {cartasSelecionadas.length}/{cartasNecessarias}
                      </p>
                    </div>

                    <div className="flex gap-2 flex-wrap">
                      <button
                        type="button"
                        className="flex-1 min-w-[180px] bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:bg-gray-300 disabled:text-gray-600"
                        onClick={conquistarRota}
                        disabled={
                          cartasSelecionadas.length !== cartasNecessarias ||
                          fluxoBilhetesAtivo ||
                          carregandoBilhetesPreview ||
                          acaoCartasBloqueiaOutras
                        }
                      >
                        Conquistar rota selecionada
                      </button>
                      <button
                        type="button"
                        className="flex-1 min-w-[160px] bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg transition-colors"
                        onClick={() => setCartasSelecionadas([])}
                      >
                        Limpar seleção
                      </button>
                    </div>
                  </div>
                )
              }}
            />

            {/* Minhas cartas */}
            <div className="mt-4 bg-white rounded-lg shadow-xl p-4">
              <h2 className="text-xl font-bold mb-4 text-gray-900">Suas Cartas</h2>
              {minhasCartas.length > 0 ? (
                <MaoCartas
                  jogadorNome={jogadorAtual?.nome || "Você"}
                  cartas={minhasCartas.map((c, i) => ({
                    id: `carta-${i}`,
                    cor: c.cor as any,
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

            {/* Rotas Conquistadas */}
            <div className="mt-4 bg-white rounded-lg shadow-xl p-4">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-3">
                <h2 className="text-xl font-bold text-gray-900">Rotas Conquistadas</h2>
                <span className="text-sm font-semibold text-green-700">
                  Pontos em rotas: {totalPontosRotas}
                </span>
              </div>
              {rotasConquistadas.length === 0 ? (
                <p className="text-sm text-gray-500">
                  Ainda não há rotas conquistadas. Use cartas para dominar o mapa!
                </p>
              ) : (
                <ul className="space-y-2">
                  {rotasConquistadas.map((rota) => (
                    <li
                      key={rota.id}
                      className="flex items-center justify-between rounded-lg border border-green-100 bg-green-50 px-3 py-2 text-sm"
                    >
                      <div className="flex flex-col">
                        <span className="font-semibold text-gray-800">
                          {rota.origem} → {rota.destino}
                        </span>
                        <span className="text-xs text-gray-600">
                          {rota.comprimento} vagões
                        </span>
                      </div>
                      <span className="text-sm font-bold text-green-700">+{rota.pontos} pts</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* Bilhetes de Destino */}
            <div className="mt-4">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 gap-1">
                <span className="text-sm font-semibold text-gray-700">
                  Bilhetes de destino de {jogadorAtual?.nome || "jogador"}
                </span>
                <span className="text-xs uppercase tracking-wide text-gray-500">
                  Atualiza automaticamente ao completar rotas
                </span>
              </div>
              <PainelBilhetesDestino
                bilhetes={bilhetesAtuais.map(b => ({
                  id: b.id,
                  origem: b.cidadeOrigem,
                  destino: b.cidadeDestino,
                  pontos: b.pontos,
                  completo: b.completo || false
                }))}
                jogadorNome={jogadorAtual?.nome || "Jogador"}
                modoSecreto={false}
                isExpanded={true}
                mostrarStatus={true}
              />
            </div>
          </div>
        </div>
      </div>
      </div>
      <TelaFimJogo
        pontuacoes={pontuacaoFinal}
        exibir={mostrarTelaFimJogo && pontuacaoFinal.length > 0}
        onJogarNovamente={handleJogarNovamente}
        onVoltarMenu={handleVoltarMenu}
      />
    </>
  )
}
