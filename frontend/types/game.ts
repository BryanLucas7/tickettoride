/**
 * Tipos e Interfaces do Domínio do Jogo
 * 
 * Este arquivo centraliza todas as interfaces e constantes
 * relacionadas ao estado do jogo Ticket to Ride.
 * 
 * CONVENÇÕES DE TIPOS:
 * - Use `interface` para: objetos, props de componentes, contratos de API
 * - Use `type` para: union types, aliases, tipos utilitários
 * - Use `enum` para: conjuntos fixos de valores conhecidos em compile-time
 * - Use `Branded Types` para: IDs únicos de entidades (JogadorId, GameId, etc.)
 */

import type { JogadorId, GameId, RotaId, BilheteId } from './branded'

// Re-export branded types para conveniência
export type { JogadorId, GameId, RotaId, BilheteId } from './branded'
export { asJogadorId, asGameId, asRotaId, asBilheteId } from './branded'

// ============================================
// ENUMS
// ============================================

/**
 * Enum de cores de cartas de vagão
 * Usado para representação visual em componentes UI
 */
export enum CorCarta {
  VERMELHO = 'VERMELHO',
  AZUL = 'AZUL',
  VERDE = 'VERDE',
  AMARELO = 'AMARELO',
  LARANJA = 'LARANJA',
  BRANCO = 'BRANCO',
  PRETO = 'PRETO',
  ROXO = 'ROXO',
  LOCOMOTIVA = 'LOCOMOTIVA'
}

// ============================================
// UNION TYPES (usar `type` para unions)
// ============================================

/**
 * Status possíveis do turno do jogador
 */
export type StatusTurno = 
  | 'aguardando'           // Não é vez do jogador
  | 'comprando_cartas'     // Jogador está comprando cartas
  | 'conquistando_rota'    // Jogador está tentando conquistar rota
  | 'comprando_bilhetes'   // Jogador está escolhendo bilhetes

/**
 * Status possíveis do jogo
 */
export type StatusJogo = 
  | 'configurando'    // Setup inicial
  | 'em_andamento'    // Jogo ativo
  | 'ultima_rodada'   // Última rodada (alguém com ≤2 trens)
  | 'finalizado'      // Jogo encerrado

/**
 * Cores válidas para jogadores
 */
export type CorJogador = 'vermelho' | 'azul' | 'verde' | 'amarelo' | 'roxo'

/**
 * Cores válidas para rotas (inclui cinza para rotas neutras)
 */
export type CorRotaString = 'vermelho' | 'azul' | 'verde' | 'amarelo' | 'laranja' | 'branco' | 'preto' | 'roxo' | 'cinza'

/**
 * Cores válidas para cartas de vagão (string union)
 * Diferente do enum CorCarta, este type usa lowercase para compatibilidade com backend
 */
export type CorCartaString = 'vermelho' | 'azul' | 'verde' | 'amarelo' | 'laranja' | 'branco' | 'preto' | 'roxo' | 'locomotiva'

// ============================================
// INTERFACES DE ENTIDADES
// ============================================

/**
 * Representa um jogador no jogo
 */
export interface Jogador {
  id: JogadorId
  nome: string
  cor: CorJogador
  trens_disponiveis: number
  pontos: number
}

/**
 * Representa uma carta de vagão (trem) - interface canônica
 * Cor é string lowercase para compatibilidade com backend
 */
export interface CartaVagao {
  cor: CorCartaString
  eh_locomotiva?: boolean
}

/**
 * Carta de vagão para componentes UI (usa enum CorCarta)
 */
export interface CartaVagaoUI {
  cor: CorCarta
  id?: string
}

/**
 * Normaliza string de cor para enum CorCarta
 */
export function toCorCarta(cor: string): CorCarta {
  const corUpper = cor.toUpperCase()
  if (corUpper in CorCarta) {
    return CorCarta[corUpper as keyof typeof CorCarta]
  }
  return CorCarta.LOCOMOTIVA
}

/**
 * Converte CartaVagao para CartaVagaoUI
 */
export function toCartaVagaoUI(carta: CartaVagao, id?: string): CartaVagaoUI {
  return {
    cor: toCorCarta(carta.cor),
    id
  }
}

/**
 * Representa uma rota no mapa
 */
export interface Rota {
  id: RotaId
  cidadeA: string
  cidadeB: string
  comprimento: number
  cor: CorRotaString
  proprietario_id: JogadorId | null
  proprietario_nome: string | null
  proprietario_cor: CorJogador | null
  conquistada: boolean
}

/**
 * Representa um bilhete de destino (objetivo)
 * 
 * Esta é a interface canônica - use esta em todo o projeto.
 * Para componentes que usam origem/destino, use a função auxiliar
 * ou mapeie os campos.
 */
export interface BilheteDestino {
  id: BilheteId
  cidadeOrigem: string
  cidadeDestino: string
  pontos: number
  index: number
  completo?: boolean
}

/**
 * Interface alternativa para componentes UI que usam origem/destino
 * @deprecated Prefira usar BilheteDestino e mapear os campos
 */
export interface BilheteDestinoUI {
  id: BilheteId
  origem: string
  destino: string
  pontos: number
  completo: boolean
}

/**
 * Converte BilheteDestino para formato UI
 */
export function toBilheteDestinoUI(bilhete: BilheteDestino): BilheteDestinoUI {
  return {
    id: bilhete.id,
    origem: bilhete.cidadeOrigem,
    destino: bilhete.cidadeDestino,
    pontos: bilhete.pontos,
    completo: bilhete.completo ?? false
  }
}

/**
 * Representa um líder do maior caminho
 */
export interface MaiorCaminhoLeader {
  jogador_id: JogadorId
  jogador_nome: string
  jogador_cor: CorJogador
}

/**
 * Status do maior caminho no jogo
 */
export interface MaiorCaminhoStatus {
  comprimento: number
  lideres: MaiorCaminhoLeader[]
  caminho?: string[]
}

/**
 * Estado completo do jogo
 */
export interface GameState {
  game_id: GameId
  iniciado: boolean
  finalizado: boolean
  jogadores: Jogador[]
  jogador_atual_id: JogadorId | null
  cartas_visiveis: CartaVagao[]
  cartas_fechadas_restantes?: number
  cartas_fechadas_disponiveis?: number
  pode_comprar_carta_fechada?: boolean
  bilhetes_restantes?: number
  maior_caminho?: MaiorCaminhoStatus
}

// ============================================
// CONSTANTES DE CONFIGURAÇÃO
// ============================================

/**
 * Pontuação por comprimento de rota
 */
export const PONTOS_ROTA: Record<number, number> = {
  1: 1,
  2: 2,
  3: 4,
  4: 7,
  5: 10,
  6: 15
}

/**
 * Tipo para chaves válidas do mapa de cores
 */
export type CorMapa = CorJogador | CorCartaString | CorRotaString | 'rosa'

/**
 * Mapeamento de cores do português para inglês (para UI)
 * Inclui cores de jogadores, cartas e rotas
 */
export const MAPA_CORES_FINAIS: Record<CorMapa, string> = {
  vermelho: "red",
  azul: "blue",
  verde: "green",
  amarelo: "yellow",
  roxo: "purple",
  laranja: "orange",
  rosa: "pink",
  preto: "black",
  branco: "white",
  cinza: "teal",
  locomotiva: "gray"
}

/**
 * Type guard para verificar se uma string é uma cor válida do mapa
 */
export function isCorMapa(cor: string): cor is CorMapa {
  return cor in MAPA_CORES_FINAIS
}

/**
 * Obtém a cor em inglês de forma type-safe
 * @param cor Cor em português
 * @param fallback Cor de fallback (padrão: "gray")
 */
export function obterCorMapa(cor: string | null | undefined, fallback = "gray"): string {
  if (!cor) return fallback
  const normalizada = cor.toLowerCase()
  return isCorMapa(normalizada) ? MAPA_CORES_FINAIS[normalizada] : fallback
}

// ============================================
// CONSTANTES DE INFRAESTRUTURA
// ============================================

/**
 * URL padrão da API
 */
export const DEFAULT_API_URL = "http://localhost:8000"

/**
 * Chave do localStorage para o ID do jogo
 */
export const GAME_STORAGE_KEY = "gameId"
