"use client"

/**
 * JogoPage - Página principal do jogo Ticket to Ride
 * 
 * Este componente foi refatorado seguindo GRASP principles:
 * - SRP: Responsabilidade única de orquestrar a UI do jogo
 * - Low Coupling: Usa useGameEngine para toda lógica de negócio
 * - High Cohesion: Componentes visuais extraídos para arquivos próprios
 * 
 * Refatorações aplicadas:
 * - JogoLoading e JogoError extraídos para components/
 * - useMapaLoader extraído para hooks/
 * - TelaFimJogo com lazy loading para melhor performance inicial
 * 
 * Redução: 1331 linhas → ~200 linhas
 */

import { useRouter } from "next/navigation"
import dynamic from "next/dynamic"
import { PONTOS_ROTA } from "@/types/game"
import { getCoresBgClass, getLetraCor, getCorTextoClass } from "@/lib/gameRules"
import { useGameEngine } from "@/hooks/useGameEngine"
import { useMapaLoader } from "./hooks/useMapaLoader"
import { JogoLoading, JogoError } from "./components"

// Componentes extraídos
import {
  GameHeader,
  ListaJogadores,
  MaiorCaminhoWidget,
  AcoesDoTurno,
  RotaDetalhesPanel,
  MinhasCartasPanel,
  RotasConquistadasPanel,
  Board,
  PainelBilhetesDestino
} from "@/features/game/components"

// Lazy loading para TelaFimJogo - só carrega quando necessário
// Melhora o tempo de carregamento inicial da página
const TelaFimJogo = dynamic(
  () => import("@/features/game/components/TelaFimJogo"),
  { 
    loading: () => null, // Não mostra loading pois só aparece no fim
    ssr: false // Não precisa de SSR
  }
)

// ============================================
// COMPONENTE PRINCIPAL
// ============================================

export default function JogoPage() {
  const router = useRouter()
  
  // Hook compositor que gerencia todo o estado do jogo
  const game = useGameEngine()
  
  // Hook para carregamento do mapa (extraído para SRP)
  const { mapa, carregandoMapa } = useMapaLoader()
  
  // Aliases para funções de cor (compatibilidade)
  const getCoresBg = getCoresBgClass
  const getCorTexto = getCorTextoClass

  // ============================================
  // RENDERIZAÇÃO CONDICIONAL - LOADING
  // ============================================
  
  if (game.carregando) {
    return <JogoLoading />;
  }

  // ============================================
  // RENDERIZAÇÃO CONDICIONAL - ERRO
  // ============================================
  
  if (!game.gameState) {
    return (
      <JogoError 
        mensagem={game.mensagem} 
        onVoltar={() => router.push("/")} 
      />
    );
  }

  // ============================================
  // VALORES DERIVADOS
  // ============================================
  
  const { gameState } = game
  const meuJogadorId = game.jogadorAtualId
  const meuJogador = gameState.jogadores.find(j => j.id === meuJogadorId)
  const ehMinhaVez = game.ehMinhaVez // Agora validado com backend
  const cartasCompradasNoTurno = game.turnoCompraCompleto ? 2 : game.cartasCompradasNesteTurno
  const cartasFechadasRestantes = gameState.cartas_fechadas_disponiveis ?? gameState.cartas_fechadas_restantes ?? null
  
  const rotasConquistadas = game.rotasDoJogo
    .filter((rota) => rota.proprietario_id === meuJogadorId)
    .map((rota) => ({
      id: rota.id,
      origem: rota.cidadeA,
      destino: rota.cidadeB,
      comprimento: rota.comprimento,
      pontos: PONTOS_ROTA[rota.comprimento] || 0
    }))
  
  const totalPontosRotas = rotasConquistadas.reduce((acc, rota) => acc + rota.pontos, 0)
  
  const mensagemPrincipal = gameState.finalizado
    ? game.mensagemFimJogo || "🏁 Jogo finalizado! Veja o resultado final."
    : game.mensagem

  // ============================================
  // RENDERIZAÇÃO PRINCIPAL
  // ============================================
  
  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-4">
        <div className="container mx-auto px-4">
          {/* Header */}
          <GameHeader
            mensagem={mensagemPrincipal}
            ehMinhaVez={ehMinhaVez}
            onSair={() => router.push("/")}
          />

          <div className="grid lg:grid-cols-3 gap-4">
            {/* Coluna esquerda - Jogadores e Ações */}
            <div className="space-y-4">
            {/* Lista de Jogadores */}
            <ListaJogadores
              gameState={gameState}
              jogadorAtualId={meuJogadorId}
              getCoresBg={getCoresBg}
            />

              {/* Widget Maior Caminho */}
              <MaiorCaminhoWidget gameState={gameState} />

              {/* Ações do turno */}
              {ehMinhaVez && (
                <AcoesDoTurno
                  game={game}
                  gameState={gameState}
                  cartasCompradasNoTurno={cartasCompradasNoTurno}
                  cartasFechadasRestantes={cartasFechadasRestantes}
                  getCoresBg={getCoresBg}
                  getCorTexto={getCorTexto}
                  getLetraCor={getLetraCor}
                />
              )}
            </div>

            {/* Coluna central - Mapa */}
            <div className="lg:col-span-2">
              {mapa ? (
                <Board
                  mapa={mapa}
                  rotasDoJogo={game.rotasDoJogo}
                  rotaSelecionadaId={game.rotaSelecionada}
                  onRotaSelecionada={game.handleSelecaoRotaMapa}
                  renderRotaDetalhes={({ rotaMapa, rotaDoJogo }) => (
                    <RotaDetalhesPanel
                      rotaMapa={rotaMapa}
                      rotaDoJogo={rotaDoJogo}
                      game={game}
                      ehMinhaVez={ehMinhaVez}
                      getCoresBg={getCoresBg}
                      getCorTexto={getCorTexto}
                      getLetraCor={getLetraCor}
                    />
                  )}
                />
              ) : (
                <div className="bg-white rounded-lg shadow-xl p-6 border border-gray-200 text-gray-700">
                  {carregandoMapa
                    ? "Carregando definição do mapa..."
                    : "Não foi possível carregar o mapa canônico do backend. Verifique se a API está ativa."}
                </div>
              )}
            </div>

            {/* Minhas cartas */}
            <MinhasCartasPanel
              jogadorNome={meuJogador?.nome || "Você"}
              cartas={game.minhasCartas}
            />

            {/* Rotas Conquistadas */}
            <RotasConquistadasPanel
              rotasConquistadas={rotasConquistadas}
              totalPontos={totalPontosRotas}
            />

            {/* Bilhetes de Destino */}
            <div className="mt-4">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 gap-1">
                <span className="text-sm font-semibold text-gray-700">
                  Bilhetes de destino de {meuJogador?.nome || "jogador"}
                </span>
                <span className="text-xs uppercase tracking-wide text-gray-500">
                  Atualiza automaticamente ao completar rotas
                </span>
              </div>
              <PainelBilhetesDestino
                bilhetes={game.meusBilhetes.map(b => ({
                  id: b.id,
                  origem: b.cidadeOrigem,
                  destino: b.cidadeDestino,
                  pontos: b.pontos,
                  completo: b.completo || false
                }))}
                jogadorNome={meuJogador?.nome || "Jogador"}
                modoSecreto={false}
                isExpanded={true}
                mostrarStatus={true}
              />
            </div>
          </div>
        </div>
      </div>
      
      {/* Tela de Fim de Jogo */}
      <TelaFimJogo
        pontuacoes={game.pontuacaoFinal}
        exibir={game.mostrarTelaFimJogo && game.pontuacaoFinal.length > 0}
        onJogarNovamente={game.handleJogarNovamente}
        onVoltarMenu={game.handleVoltarMenu}
      />
    </>
  )
}
