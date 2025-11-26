/**
 * CONTADOR DE TRENS RESTANTES - Componente UI
 * ============================================
 * 
 * Exibe quantidade de trens restantes de cada jogador.
 * Alerta visual quando jogador tem ≤2 trens (fim de jogo iminente).
 * 
 * Princípios GRASP aplicados:
 * - Information Expert: Jogador possui e gerencia seus trens
 * - High Cohesion: Componente focado apenas em exibir contadores de trens
 * - Low Coupling: Não conhece lógica de conquista de rotas
 * 
 * Padrão GoF: Observer Pattern - Observa mudanças no número de trens
 */

'use client';

import { useChangeAnimation } from '@/hooks/useChangeAnimation';
import type { ContadorTrensProps } from './types';
import { useAlertaFimJogo } from './hooks/useAlertaFimJogo';
import { ModoExpandido } from './ModoExpandido';
import { ModoCompacto } from './ModoCompacto';

/**
 * Componente Principal
 * 
 * GRASP - Information Expert:
 * Jogador conhece seus trens, componente apresenta essa informação
 * 
 * GRASP - High Cohesion:
 * Focado apenas em exibir contador de trens
 * 
 * Observer Pattern:
 * Reage a mudanças no número de trens dos jogadores
 */
export function ContadorTrens({
    jogadores,
    trensIniciais = 45,
    limiteAlerta = 2,
    modo = 'expandido',
    mostrarBarras = true,
    animarMudancas = true
}: ContadorTrensProps) {
    // Usa hooks personalizados para detectar mudanças e alertas
    // Corrige problema de dependência circular com useRef interno
    const mudancas = useChangeAnimation(
        jogadores,
        (jogador) => jogador.trensRestantes,
        { animationDuration: 2000, enabled: animarMudancas }
    );

    const alertaFimJogo = useAlertaFimJogo(jogadores, limiteAlerta);

    if (modo === 'compacto') {
        return (
            <ModoCompacto
                jogadores={jogadores}
                limiteAlerta={limiteAlerta}
                mudancas={mudancas}
            />
        );
    }

    return (
        <ModoExpandido
            jogadores={jogadores}
            trensIniciais={trensIniciais}
            limiteAlerta={limiteAlerta}
            mostrarBarras={mostrarBarras}
            mudancas={mudancas}
            alertaFimJogo={alertaFimJogo}
        />
    );
}

// Export padrão para compatibilidade
export default ContadorTrens;
