/**
 * TRILHA DE PONTUAÇÃO VISUAL - Componente UI
 * ===========================================
 * 
 * Exibe a pontuação de cada jogador em tempo real com marcadores coloridos.
 * Pode ser renderizada como trilha circular ao redor do mapa ou painel lateral.
 * 
 * Princípios GRASP aplicados:
 * - Information Expert: Placar calcula e gerencia pontos dos jogadores
 * - Low Coupling: UI apenas observa mudanças no placar
 * - High Cohesion: Componente focado apenas em exibir pontuação
 * 
 * Padrão GoF: Observer Pattern - Observa mudanças no placar e atualiza UI
 */

'use client';

import { useChangeAnimation } from '@/hooks/useChangeAnimation';
import type { TrilhaPontuacaoProps } from './types';
import { PainelLateral } from './PainelLateral';
import { TrilhaCircular } from './TrilhaCircular';

/**
 * Componente Principal
 * 
 * GRASP - Information Expert:
 * Recebe dados do placar e apresenta pontuação de forma visual
 * 
 * GRASP - Low Coupling:
 * Não conhece lógica de cálculo de pontos, apenas apresenta
 * 
 * Observer Pattern:
 * Reage a mudanças no array de jogadores (pontos)
 */
export function TrilhaPontuacao({
    jogadores,
    maxPontos = 100,
    modo = 'painel',
    largura = 600,
    altura = 600,
    animarMudancas = true,
    mostrarNomes = true
}: TrilhaPontuacaoProps) {
    // Usa hook personalizado para detectar e animar mudanças de pontuação
    // Corrige problema de dependência circular com useRef interno
    const mudancas = useChangeAnimation(
        jogadores,
        (jogador) => jogador.pontos,
        { animationDuration: 2000, enabled: animarMudancas }
    );

    // Renderiza modo apropriado
    if (modo === 'trilha') {
        return (
            <TrilhaCircular
                jogadores={jogadores}
                maxPontos={maxPontos}
                largura={largura}
                altura={altura}
                mudancas={mudancas}
            />
        );
    }

    return (
        <PainelLateral
            jogadores={jogadores}
            maxPontos={maxPontos}
            mudancas={mudancas}
            mostrarNomes={mostrarNomes}
        />
    );
}

// Export padrão para compatibilidade
export default TrilhaPontuacao;
