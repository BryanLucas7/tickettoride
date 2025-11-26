/**
 * Tipos compartilhados para ContadorTrens
 */

/**
 * Interface do Jogador para contador de trens
 */
export interface JogadorTrens {
    id: string;
    nome: string;
    trensRestantes: number;
    cor: string; // Cor visual do jogador
}

/**
 * Props do Componente principal
 */
export interface ContadorTrensProps {
    jogadores: JogadorTrens[];
    trensIniciais?: number;      // Quantidade inicial de trens (padrão: 45)
    limiteAlerta?: number;       // Alerta quando trens <= este valor (padrão: 2)
    modo?: 'compacto' | 'expandido'; // Modo de visualização
    mostrarBarras?: boolean;     // Mostra barras de progresso
    animarMudancas?: boolean;    // Anima mudanças
}

/**
 * Props do ModoExpandido
 */
export interface ModoExpandidoProps {
    jogadores: JogadorTrens[];
    trensIniciais: number;
    limiteAlerta: number;
    mostrarBarras: boolean;
    mudancas: Record<string, number>;
    alertaFimJogo: boolean;
}

/**
 * Props do ModoCompacto
 */
export interface ModoCompactoProps {
    jogadores: JogadorTrens[];
    limiteAlerta: number;
    mudancas: Record<string, number>;
}

/**
 * Props do JogadorTrensItem
 */
export interface JogadorTrensItemProps {
    jogador: JogadorTrens;
    trensIniciais: number;
    limiteAlerta: number;
    mostrarBarras: boolean;
    mudanca?: number;
}

/**
 * Props do JogadorTrensCompactoItem
 */
export interface JogadorTrensCompactoItemProps {
    jogador: JogadorTrens;
    limiteAlerta: number;
    mudanca?: number;
}
