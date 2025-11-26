/**
 * Botão individual de carta visível
 * 
 * GRASP - High Cohesion: Encapsula toda lógica de estado de um botão de carta
 */

import type { CartaVisivelButtonProps } from './types';

/**
 * Botão para comprar carta visível
 */
export function CartaVisivelButton({
    carta,
    index,
    desabilitada,
    bloqueadaLocomotiva,
    turnoCompraCompleto,
    titulo,
    onClick,
    getCoresBg,
    getCorTexto,
    getLetraCor
}: CartaVisivelButtonProps) {
    const corNormalizada = carta.cor.toLowerCase();
    const ehLocomotiva = carta.eh_locomotiva === true || corNormalizada === "locomotiva";

    return (
        <button
            key={index}
            type="button"
            onClick={onClick}
            disabled={desabilitada}
            className={`relative w-16 h-20 rounded-lg flex items-center justify-center text-xs font-bold transition-all ${getCoresBg(carta.cor)
                } ${getCorTexto(carta.cor)} shadow-md hover:scale-105 hover:ring-2 hover:ring-green-400 disabled:hover:scale-100 disabled:hover:ring-0 disabled:cursor-not-allowed disabled:opacity-40 ${bloqueadaLocomotiva && ehLocomotiva ? "ring-2 ring-amber-400 ring-offset-2 ring-offset-white" : ""
                }`}
            title={titulo}
        >
            {getLetraCor(carta.cor)}
            {bloqueadaLocomotiva && ehLocomotiva && !turnoCompraCompleto && (
                <span className="absolute -top-1 -right-1 bg-amber-100 text-amber-700 text-[10px] font-semibold px-1 py-[1px] rounded-full border border-amber-300">
                    ⚠️
                </span>
            )}
        </button>
    );
}
