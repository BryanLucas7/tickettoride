/**
 * CAMADA DE DOMÍNIO - REGRAS DO JOGO
 * ====================================
 * 
 * Contém a lógica pura de negócio do jogo Ticket to Ride.
 * Não depende de React, estado ou UI.
 * 
 * Benefícios:
 * - Testável unitariamente sem renderização de componentes
 * - Reutilizável em diferentes contextos
 * - Separação clara entre lógica de negócio e apresentação
 */

import { type CartaVagao, type Rota, PONTOS_ROTA, obterCorMapa } from '@/types/game';

// ============================================
// TIPOS DE RESULTADO
// ============================================

/**
 * Resultado da validação de seleção de cartas para rota
 */
export interface ValidacaoRotaResult {
  valida: boolean;
  mensagem?: string;
  cartasDetalhes?: CartaVagao[];
}

/**
 * Resultado da validação de regras de locomotiva
 */
export interface ValidacaoLocomotivaResult {
  permitido: boolean;
  mensagem?: string;
}

// ============================================
// VALIDAÇÃO DE ROTAS
// ============================================

/**
 * Valida se a seleção de cartas é válida para conquistar uma rota
 * 
 * Regras:
 * 1. Deve haver uma rota selecionada
 * 2. Todas as cartas selecionadas devem existir na mão
 * 3. Quantidade de cartas deve ser igual ao comprimento da rota
 * 4. Para rotas coloridas: cartas devem ser da cor da rota ou locomotivas
 * 5. Para rotas cinza: cartas devem ser todas da mesma cor (ou locomotivas)
 */
export function validarSelecaoCartasParaRota(
  rotaInfo: Rota | null,
  cartasSelecionadas: CartaVagao[]
): ValidacaoRotaResult {
  // 1. Verifica se há rota selecionada
  if (!rotaInfo) {
    return {
      valida: false,
      mensagem: "❌ Selecione uma rota disponível no mapa antes de conquistar"
    };
  }

  // 2. Verifica se todas as cartas existem
  const cartasValidas = cartasSelecionadas.filter((carta): carta is CartaVagao => Boolean(carta));
  if (cartasValidas.length !== cartasSelecionadas.length) {
    return {
      valida: false,
      mensagem: "❌ Não foi possível localizar todas as cartas selecionadas. Atualize as cartas e tente novamente."
    };
  }

  // 3. Verifica quantidade de cartas
  if (cartasValidas.length !== rotaInfo.comprimento) {
    return {
      valida: false,
      mensagem: `❌ Selecione ${rotaInfo.comprimento} carta${rotaInfo.comprimento > 1 ? "s" : ""} para conquistar esta rota.`
    };
  }

  // 4-5. Valida cores das cartas
  const validacaoCores = validarCoresParaRota(rotaInfo, cartasValidas);
  if (!validacaoCores.valida) {
    return validacaoCores;
  }

  return { valida: true, cartasDetalhes: cartasValidas };
}

/**
 * Valida se as cores das cartas são compatíveis com a rota
 */
function validarCoresParaRota(
  rotaInfo: Rota,
  cartas: CartaVagao[]
): ValidacaoRotaResult {
  const corRota = rotaInfo.cor.toLowerCase();
  
  // Separa locomotivas das cartas normais
  const coresNaoLocomotiva = new Set(
    cartas
      .filter((carta) => !carta.eh_locomotiva)
      .map((carta) => carta.cor.toLowerCase())
  );

  // Rotas cinza: cartas devem ser todas da mesma cor
  if (corRota === "cinza") {
    if (coresNaoLocomotiva.size > 1) {
      return {
        valida: false,
        mensagem: "❌ Rotas cinza exigem cartas da mesma cor. Use locomotivas como coringa para completar."
      };
    }
    return { valida: true };
  }

  // Rotas coloridas: cartas devem ser da cor da rota ou locomotivas
  const temCorIncorreta = Array.from(coresNaoLocomotiva).some((cor) => cor !== corRota);
  if (temCorIncorreta) {
    return {
      valida: false,
      mensagem: `❌ Use cartas ${corRota} ou locomotivas para esta rota.`
    };
  }

  return { valida: true };
}

// PONTUAÇÃO
// ============================================

/**
 * Normaliza cor para uso no fim do jogo (português -> inglês)
 */
export function normalizarCorParaUI(cor?: string | null): string {
  if (!cor) return "blue";
  return obterCorMapa(cor, "blue");
}

// ============================================
// UTILITÁRIOS DE COR
// ============================================

/**
 * Retorna a classe CSS de background para uma cor de carta
 */
export function getCoresBgClass(cor: string): string {
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
  };
  return cores[cor.toLowerCase()] || "bg-gray-500";
}

/**
 * Retorna a letra representativa de uma cor
 */
export function getLetraCor(cor: string): string {
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
  };
  return letras[cor.toLowerCase()] || cor.charAt(0).toUpperCase();
}

/**
 * Retorna a classe CSS de texto para uma cor de carta
 */
export function getCorTextoClass(cor: string): string {
  // Cartas brancas usam texto preto
  if (cor.toLowerCase() === "branco") {
    return "text-gray-900";
  }
  return "text-white";
}
