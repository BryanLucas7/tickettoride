/**
 * Componente de Alerta de Fim de Jogo
 * Badge visual que indica que o fim do jogo está próximo
 */

interface AlertaFimJogoProps {
    visivel: boolean;
}

/**
 * Badge de alerta animado para fim de jogo iminente
 */
export function AlertaFimJogo({ visivel }: AlertaFimJogoProps) {
    if (!visivel) return null;

    return (
        <div className="bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold animate-pulse">
            ⚠️ FIM PRÓXIMO
        </div>
    );
}
