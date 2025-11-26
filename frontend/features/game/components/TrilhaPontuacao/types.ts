/**
 * Tipos compartilhados para TrilhaPontuacao
 */

/**
 * Interface de Jogador para exibição no placar
 */
export interface JogadorPlacar {
    id: string;
    nome: string;
    pontos: number;
    cor: string; // Cor do marcador (ex: 'red', 'blue', 'green', 'yellow', 'purple')
}

/**
 * Props do Componente principal
 */
export interface TrilhaPontuacaoProps {
    jogadores: JogadorPlacar[];
    maxPontos?: number;        // Pontos máximos da trilha (padrão: 100)
    modo?: 'trilha' | 'painel'; // Modo de visualização
    largura?: number;           // Largura em pixels (modo trilha)
    altura?: number;            // Altura em pixels (modo trilha)
    animarMudancas?: boolean;   // Anima mudanças de pontuação
    mostrarNomes?: boolean;     // Mostra nomes dos jogadores
}

/**
 * Props do PainelLateral
 */
export interface PainelLateralProps {
    jogadores: JogadorPlacar[];
    maxPontos: number;
    mudancas: Record<string, number>;
    mostrarNomes: boolean;
}

/**
 * Props do TrilhaCircular
 */
export interface TrilhaCircularProps {
    jogadores: JogadorPlacar[];
    maxPontos: number;
    largura: number;
    altura: number;
    mudancas: Record<string, number>;
}

/**
 * Props do MarcadorJogador (para TrilhaCircular)
 */
export interface MarcadorJogadorProps {
    jogador: JogadorPlacar;
    posicao: { x: number; y: number };
    mudanca?: number;
}
