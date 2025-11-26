/**
 * Configuração visual de cores de cartas
 * 
 * Responsabilidade única: Definir estilos visuais para cada cor
 */

import { CorCarta } from '@/types/game';

export interface CorConfig {
  bg: string;
  border: string;
  text: string;
  label: string;
  emoji: string;
}

// Constantes de texto para evitar duplicação
const TEXT_WHITE = 'text-white';
const TEXT_DARK = 'text-gray-900';

export const CORES_CONFIG: Record<CorCarta, CorConfig> = {
  [CorCarta.VERMELHO]: {
    bg: 'bg-red-500',
    border: 'border-red-700',
    text: TEXT_WHITE,
    label: 'Vermelho',
    emoji: '🔴'
  },
  [CorCarta.AZUL]: {
    bg: 'bg-blue-500',
    border: 'border-blue-700',
    text: TEXT_WHITE,
    label: 'Azul',
    emoji: '🔵'
  },
  [CorCarta.VERDE]: {
    bg: 'bg-green-500',
    border: 'border-green-700',
    text: TEXT_WHITE,
    label: 'Verde',
    emoji: '🟢'
  },
  [CorCarta.AMARELO]: {
    bg: 'bg-yellow-400',
    border: 'border-yellow-600',
    text: TEXT_DARK,
    label: 'Amarelo',
    emoji: '🟡'
  },
  [CorCarta.LARANJA]: {
    bg: 'bg-orange-500',
    border: 'border-orange-700',
    text: TEXT_WHITE,
    label: 'Laranja',
    emoji: '🟠'
  },
  [CorCarta.BRANCO]: {
    bg: 'bg-gray-100',
    border: 'border-gray-400',
    text: TEXT_DARK,
    label: 'Branco',
    emoji: '⚪'
  },
  [CorCarta.PRETO]: {
    bg: 'bg-gray-900',
    border: 'border-gray-700',
    text: TEXT_WHITE,
    label: 'Preto',
    emoji: '⚫'
  },
  [CorCarta.ROXO]: {
    bg: 'bg-purple-500',
    border: 'border-purple-700',
    text: TEXT_WHITE,
    label: 'Roxo',
    emoji: '🟣'
  },
  [CorCarta.LOCOMOTIVA]: {
    bg: 'bg-gradient-to-br from-purple-600 to-pink-600',
    border: 'border-purple-800',
    text: TEXT_WHITE,
    label: 'Locomotiva',
    emoji: '🚂'
  }
};

export function getCorConfig(cor: CorCarta): CorConfig {
  return CORES_CONFIG[cor];
}
