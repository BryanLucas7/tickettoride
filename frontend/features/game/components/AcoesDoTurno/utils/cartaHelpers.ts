/**
 * cartaHelpers - Funções auxiliares para lógica de cartas
 * 
 * GRASP - Information Expert: Encapsula regras de negócio sobre cartas
 * 
 * Extraído de SecaoCompraCartas.tsx para seguir SRP
 */

import type { UseGameEngineReturn } from "@/hooks/useGameEngine";

/**
 * Interface simplificada do estado do jogo necessário para helpers
 */
interface GameStateForHelpers {
  fluxoBilhetesAtivo: boolean;
  carregandoBilhetesPreview: boolean;
  turnoCompraCompleto: boolean;
  bloquearLocomotivaAberta: boolean;
  baralhoPossivelmenteVazio?: boolean;
}

/**
 * Calcula o título do tooltip para uma carta
 * 
 * @param game - Estado do jogo
 * @param ehLocomotiva - Se a carta é uma locomotiva
 * @returns Texto do tooltip ou string vazia
 */
export function calcularTituloCarta(
  game: GameStateForHelpers,
  ehLocomotiva: boolean
): string {
  if (game.fluxoBilhetesAtivo) {
    return "Finalize a escolha de bilhetes antes de comprar cartas.";
  }
  if (game.carregandoBilhetesPreview) {
    return "Aguarde o carregamento dos bilhetes.";
  }
  if (game.turnoCompraCompleto) {
    return "Você já concluiu as compras de cartas deste turno.";
  }
  if (ehLocomotiva && game.bloquearLocomotivaAberta) {
    return "Locomotiva visível bloqueada após já ter comprado uma carta.";
  }
  return "";
}

/**
 * Verifica se uma carta deve estar desabilitada
 * 
 * @param game - Estado do jogo
 * @param ehLocomotiva - Se a carta é uma locomotiva
 * @returns true se a carta está desabilitada
 */
export function cartaDesabilitada(
  game: GameStateForHelpers,
  ehLocomotiva: boolean
): boolean {
  return (
    game.turnoCompraCompleto ||
    game.fluxoBilhetesAtivo ||
    game.carregandoBilhetesPreview ||
    (game.bloquearLocomotivaAberta && ehLocomotiva)
  );
}

/**
 * Verifica se a compra de carta fechada está desabilitada
 * 
 * @param game - Estado do jogo
 * @returns true se a compra está desabilitada
 */
export function cartaFechadaDesabilitada(
  game: GameStateForHelpers
): boolean {
  return (
    game.turnoCompraCompleto ||
    game.fluxoBilhetesAtivo ||
    game.carregandoBilhetesPreview ||
    !!game.baralhoPossivelmenteVazio
  );
}

/**
 * Calcula o título do tooltip para carta fechada
 * 
 * @param game - Estado do jogo
 * @returns Texto do tooltip
 */
export function calcularTituloCartaFechada(
  game: GameStateForHelpers
): string {
  if (game.fluxoBilhetesAtivo) {
    return "Finalize a escolha de bilhetes antes de comprar cartas.";
  }
  if (game.turnoCompraCompleto) {
    return "Você já concluiu as compras de cartas deste turno.";
  }
  if (game.baralhoPossivelmenteVazio) {
    return "Baralho esgotado: não é possível comprar cartas fechadas no momento.";
  }
  return "Comprar carta do baralho fechado";
}

/**
 * Verifica se uma carta é locomotiva
 * 
 * @param carta - Objeto da carta
 * @returns true se a carta é locomotiva
 */
export function ehLocomotiva(carta: { cor: string; eh_locomotiva?: boolean }): boolean {
  const corNormalizada = carta.cor.toLowerCase();
  return carta.eh_locomotiva === true || corNormalizada === "locomotiva";
}
