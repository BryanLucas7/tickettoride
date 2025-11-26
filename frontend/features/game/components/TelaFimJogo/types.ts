/**
 * Tipos para componentes de Tela de Fim de Jogo
 */

/**
 * Interface de Bilhete para resultados
 */
export interface BilheteResultado {
  origem: string;
  destino: string;
  pontos: number;
  completo: boolean;
}

/**
 * Interface de Pontuação Final de um Jogador
 */
export interface PontuacaoFinal {
  jogadorId: string;
  jogadorNome: string;
  jogadorCor: string;
  pontosRotas: number;
  bilhetesCompletos: BilheteResultado[];
  bilhetesIncompletos: BilheteResultado[];
  pontosBilhetesPositivos: number;
  pontosBilhetesNegativos: number;
  bonusMaiorCaminho: boolean;
  pontosMaiorCaminho: number;
  pontuacaoTotal: number;
  tamanhoMaiorCaminho?: number;
}

/**
 * Props do Componente Principal
 */
export interface TelaFimJogoProps {
  pontuacoes: PontuacaoFinal[];
  exibir: boolean;
  onJogarNovamente?: () => void;
  onVoltarMenu?: () => void;
}
