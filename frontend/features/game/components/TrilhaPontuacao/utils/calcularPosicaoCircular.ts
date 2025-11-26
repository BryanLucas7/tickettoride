/**
 * Utilitário para cálculos de posição na trilha circular
 */

interface PosicaoCircular {
    x: number;
    y: number;
}

/**
 * Calcula posição X,Y na trilha circular baseado nos pontos
 * A trilha começa no topo (270°) e vai no sentido horário
 * 
 * @param pontos - Pontos atuais do jogador
 * @param maxPontos - Pontuação máxima da trilha
 * @param centroX - Coordenada X do centro
 * @param centroY - Coordenada Y do centro
 * @param raio - Raio da trilha circular
 * @returns Objeto com coordenadas x e y
 */
export function calcularPosicaoCircular(
    pontos: number,
    maxPontos: number,
    centroX: number,
    centroY: number,
    raio: number
): PosicaoCircular {
    // Trilha começa no topo (270°) e vai no sentido horário
    const angulo = 270 + (pontos / maxPontos) * 360;
    const radianos = (angulo * Math.PI) / 180;

    return {
        x: centroX + raio * Math.cos(radianos),
        y: centroY + raio * Math.sin(radianos)
    };
}
