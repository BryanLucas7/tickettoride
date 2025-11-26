/**
 * Seção de compra de cartas
 * 
 * GRASP - High Cohesion: Focado em cartas visíveis + carta fechada
 * 
 * Refatorado: Funções helper extraídas para utils/cartaHelpers.ts
 */

import type { SecaoCompraCartasProps } from './types';
import { CartaVisivelButton } from './CartaVisivelButton';
import { MensagemFeedback } from './MensagemFeedback';
import { buttonClass } from '@/lib/constants/styles';
import {
    calcularTituloCarta,
    cartaDesabilitada,
    calcularTituloCartaFechada,
    ehLocomotiva
} from './utils';

/**
 * Seção de compra de cartas - cartas visíveis e fechada
 */
export function SecaoCompraCartas({
    game,
    gameState,
    cartasCompradasNoTurno,
    cartasFechadasRestantes,
    getCoresBg,
    getCorTexto,
    getLetraCor
}: SecaoCompraCartasProps) {
    return (
        <div className="border-2 border-green-200 rounded-lg p-3">
            <h3 className="font-semibold text-green-700 mb-2">🃏 Comprar Cartas</h3>

            {/* Cartas visíveis */}
            {gameState?.cartas_visiveis && gameState.cartas_visiveis.length > 0 && (
                <div className="mb-3">
                    <p className="text-xs text-gray-600 mb-2">Escolha uma carta visível:</p>
                    <div className="flex gap-2 flex-wrap">
                        {gameState.cartas_visiveis.map((carta, index) => {
                            const isLocomotiva = ehLocomotiva(carta);
                            const desabilitada = cartaDesabilitada(game, isLocomotiva);
                            const titulo = calcularTituloCarta(game, isLocomotiva) || `Comprar carta ${carta.cor}`;

                            return (
                                <CartaVisivelButton
                                    key={index}
                                    carta={carta}
                                    index={index}
                                    desabilitada={desabilitada}
                                    bloqueadaLocomotiva={game.bloquearLocomotivaAberta}
                                    turnoCompraCompleto={game.turnoCompraCompleto}
                                    titulo={titulo}
                                    onClick={() => game.comprarCartaAberta(index)}
                                    getCoresBg={getCoresBg}
                                    getCorTexto={getCorTexto}
                                    getLetraCor={getLetraCor}
                                />
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Carta Fechada */}
            <button
                type="button"
                className={buttonClass('GREEN', 'MD', 'w-full')}
                onClick={game.comprarCartaFechada}
                disabled={game.turnoCompraCompleto || game.fluxoBilhetesAtivo || game.carregandoBilhetesPreview || game.baralhoPossivelmenteVazio}
                title={calcularTituloCartaFechada(game)}
            >
                🂠 Comprar do Baralho (Fechada)
            </button>

            <p className="text-xs text-gray-600 mt-2">
                Cartas fechadas restantes (baralho):{" "}
                {typeof cartasFechadasRestantes === "number" ? cartasFechadasRestantes : "—"}
            </p>

            <p className="text-xs text-gray-500 mt-2">
                Cartas compradas neste turno: {cartasCompradasNoTurno}/2
            </p>

            {/* Mensagens de feedback */}
            <MensagemFeedback mensagem={game.mensagemCompraCartas} tipo="warning" />

            {game.baralhoPossivelmenteVazio && (
                <MensagemFeedback
                    mensagem="Baralho esgotado: não é possível comprar cartas fechadas enquanto não houver reposição."
                    tipo="warning"
                />
            )}
        </div>
    );
}
