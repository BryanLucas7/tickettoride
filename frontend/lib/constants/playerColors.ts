/**
 * Constantes de cores dos jogadores
 * 
 * Centraliza configurações visuais de cores para evitar duplicação
 * entre componentes como ContadorTrens e TelaFimJogo.
 * 
 * GRASP - Information Expert: Arquivo único responsável por configurações de cor
 */

export interface PlayerColorConfig {
  bg: string;
  text: string;
  border: string;
}

/**
 * Mapa de cores CSS para jogadores
 * Usa classes Tailwind para estilização consistente
 */
export const CORES_JOGADORES: Record<string, PlayerColorConfig> = {
  red: { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-500' },
  blue: { bg: 'bg-blue-100', text: 'text-blue-800', border: 'border-blue-500' },
  green: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-500' },
  yellow: { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-500' },
  purple: { bg: 'bg-purple-100', text: 'text-purple-800', border: 'border-purple-500' },
  orange: { bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-500' },
  pink: { bg: 'bg-pink-100', text: 'text-pink-800', border: 'border-pink-500' },
  teal: { bg: 'bg-teal-100', text: 'text-teal-800', border: 'border-teal-500' },
  black: { bg: 'bg-gray-900', text: 'text-white', border: 'border-gray-700' },
  white: { bg: 'bg-white', text: 'text-gray-800', border: 'border-gray-300' },
};

/**
 * Retorna configuração de cor para um jogador
 * Fallback para cinza se cor não encontrada
 */
export function getPlayerColorConfig(cor: string): PlayerColorConfig {
  return CORES_JOGADORES[cor.toLowerCase()] || {
    bg: 'bg-gray-100',
    text: 'text-gray-800',
    border: 'border-gray-500'
  };
}
