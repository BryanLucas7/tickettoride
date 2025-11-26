/**
 * Hook para lógica de alerta de fim de jogo
 * Encapsula a lógica de detecção de alerta quando jogadores têm poucos trens
 */

import { useThresholdAlert } from '@/hooks/useChangeAnimation';
import type { JogadorTrens } from '../types';

/**
 * Hook customizado para detectar alerta de fim de jogo
 * 
 * @param jogadores - Lista de jogadores
 * @param limiteAlerta - Limite de trens para disparar alerta
 * @returns boolean indicando se algum jogador atingiu o limite
 */
export function useAlertaFimJogo(
    jogadores: JogadorTrens[],
    limiteAlerta: number
): boolean {
    return useThresholdAlert(
        jogadores,
        (jogador) => jogador.trensRestantes,
        limiteAlerta
    );
}
