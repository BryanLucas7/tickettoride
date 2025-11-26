/**
 * Utilitário para cálculo de altura das barras do pódio
 * 
 * Calcula altura proporcional baseada na pontuação relativa
 */

export const MIN_BAR_HEIGHT = 140;
export const MAX_BAR_HEIGHT = 280;

export interface CalculoAlturaParams {
  pontuacaoTotal: number;
  minPontuacao: number;
  maxPontuacao: number;
  totalJogadores: number;
}

/**
 * Calcula a altura da barra do pódio baseada na pontuação
 */
export function calcularAlturaBarra({
  pontuacaoTotal,
  minPontuacao,
  maxPontuacao,
  totalJogadores
}: CalculoAlturaParams): number {
  if (totalJogadores === 1) {
    return MAX_BAR_HEIGHT;
  }
  
  const faixaPontuacao = Math.max(maxPontuacao - minPontuacao, 1);
  const pesoNormalizado = (pontuacaoTotal - minPontuacao) / faixaPontuacao;
  const altura = MIN_BAR_HEIGHT + pesoNormalizado * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT);
  
  return Math.round(Math.max(MIN_BAR_HEIGHT, Math.min(MAX_BAR_HEIGHT, altura)));
}

/**
 * Estilos do pódio por posição
 */
export const PODIO_STYLES = [
  { 
    medalha: '🥇', 
    fundo: 'bg-gradient-to-b from-yellow-400 to-yellow-600', 
    borda: 'border-yellow-600', 
    largura: 'w-28' 
  },
  { 
    medalha: '🥈', 
    fundo: 'bg-gradient-to-b from-gray-300 to-gray-500', 
    borda: 'border-gray-600', 
    largura: 'w-28' 
  },
  { 
    medalha: '🥉', 
    fundo: 'bg-gradient-to-b from-amber-600 to-amber-800', 
    borda: 'border-amber-900', 
    largura: 'w-28' 
  }
];

export const ESTILO_PADRAO = {
  medalha: '🏅',
  fundo: 'bg-gradient-to-b from-gray-200 to-gray-300',
  borda: 'border-gray-400',
  largura: 'w-24'
};

export function getEstiloPodio(posicao: number) {
  return PODIO_STYLES[posicao] || ESTILO_PADRAO;
}
