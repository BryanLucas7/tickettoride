/**
 * Seção de compra de bilhetes
 * 
 * GRASP - High Cohesion: Focado em botão + estado do fluxo de bilhetes
 */

import type { SecaoCompraBilhetesProps } from './types';
import { ModalBilhetes } from '../ModalBilhetes';
import { buttonClass } from '@/lib/constants/styles';

/**
 * Calcula título do tooltip para botão de bilhetes
 */
function calcularTituloBilhetes(game: SecaoCompraBilhetesProps['game'], bilhetesRestantes: number | null): string {
    if (bilhetesRestantes !== null && bilhetesRestantes <= 0) {
        return "Baralho de bilhetes esgotado.";
    }
    if (game.fluxoBilhetesAtivo) {
        return "Finalize a escolha de bilhetes já iniciada.";
    }
    if (game.carregandoBilhetesPreview) {
        return "Carregando cartas de bilhete do baralho...";
    }
    if (game.fluxoCompraCartasAtivo) {
        return "Você já escolheu comprar cartas neste turno. Termine essa ação primeiro.";
    }
    if (game.turnoCompraCompleto) {
        return "Você já realizou uma ação neste turno. Aguarde o próximo.";
    }
    return "Comprar novos bilhetes de destino";
}

/**
 * Seção de compra de bilhetes - botão + modal
 */
export function SecaoCompraBilhetes({ game }: SecaoCompraBilhetesProps) {
    const bilhetesRestantes = game.gameState?.bilhetes_restantes ?? null;

    const desabilitado =
        game.fluxoBilhetesAtivo ||
        game.carregandoBilhetesPreview ||
        game.turnoCompraCompleto ||
        game.fluxoCompraCartasAtivo ||
        (bilhetesRestantes !== null && bilhetesRestantes <= 0);

    return (
        <>
            {/* Botão Bilhetes */}
            <button
                className={buttonClass('ORANGE', 'LG', 'w-full')}
                onClick={game.iniciarFluxoBilhetes}
                disabled={desabilitado}
                title={calcularTituloBilhetes(game, bilhetesRestantes)}
            >
                {game.carregandoBilhetesPreview ? "Carregando bilhetes..." : "🎫 Pegar Bilhetes Destino"}
            </button>

            {typeof bilhetesRestantes === "number" && (
                <p className="text-xs text-gray-600 mt-2 text-center">
                    Bilhetes restantes no baralho: {bilhetesRestantes}
                </p>
            )}

            {game.fluxoBilhetesAtivo && (
                <p className="text-xs text-orange-700 mt-2">
                    Esta ação precisa ser concluída: escolha pelo menos um bilhete para encerrar o turno.
                </p>
            )}

            {/* Modal de Bilhetes */}
            {game.mostrarModalBilhetes && (
                <ModalBilhetes game={game} />
            )}
        </>
    );
}
