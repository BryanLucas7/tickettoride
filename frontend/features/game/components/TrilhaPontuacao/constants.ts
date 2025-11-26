/**
 * Constantes para TrilhaPontuacao
 */

/**
 * Mapa de cores CSS para marcadores
 */
export const CORES_MARCADORES: Record<string, string> = {
    red: 'bg-red-500 border-red-700',
    blue: 'bg-blue-500 border-blue-700',
    green: 'bg-green-500 border-green-700',
    yellow: 'bg-yellow-400 border-yellow-600',
    purple: 'bg-purple-500 border-purple-700',
    orange: 'bg-orange-500 border-orange-700',
    pink: 'bg-pink-500 border-pink-700',
    teal: 'bg-teal-500 border-teal-700',
    indigo: 'bg-indigo-500 border-indigo-700',
    gray: 'bg-gray-500 border-gray-700',
};

/**
 * Converte cor de fundo para cor de preenchimento SVG
 * @param corClasse - Classe CSS (ex: 'bg-red-500 border-red-700')
 * @returns Classe de fill para SVG (ex: 'fill-red-500')
 */
export function corParaFill(corClasse: string): string {
    return corClasse.split(' ')[0].replace('bg-', 'fill-');
}

/**
 * Extrai classe de background de uma cor
 * @param corClasse - Classe CSS completa
 * @returns Apenas a classe bg-*
 */
export function extrairBgClasse(corClasse: string): string {
    return corClasse.split(' ')[0];
}
