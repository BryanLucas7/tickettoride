/**
 * AcoesDoTurno - Painel de ações disponíveis no turno
 * 
 * Responsabilidade: Renderizar botões e controles para comprar cartas e bilhetes
 * 
 * Princípios GRASP aplicados:
 * - High Cohesion: Componente focado em ações do turno
 * - Low Coupling: Delega responsabilidades para subcomponentes
 * 
 * Refatorado seguindo SRP: cada seção é um componente independente
 */

import type { AcoesDoTurnoProps } from './types';
import { SecaoCompraCartas } from './SecaoCompraCartas';
import { SecaoCompraBilhetes } from './SecaoCompraBilhetes';

/**
 * Componente principal - orquestra as seções de ações
 */
export function AcoesDoTurno({
    game,
    gameState,
    cartasCompradasNoTurno,
    cartasFechadasRestantes,
    getCoresBg,
    getCorTexto,
    getLetraCor
}: AcoesDoTurnoProps) {
    return (
        <div className="bg-white rounded-lg shadow-lg p-4">
            <h2 className="text-xl font-bold mb-4 text-gray-900">Ações</h2>
            <div className="space-y-3">
                {/* Seção de Compra de Cartas */}
                <SecaoCompraCartas
                    game={game}
                    gameState={gameState}
                    cartasCompradasNoTurno={cartasCompradasNoTurno}
                    cartasFechadasRestantes={cartasFechadasRestantes}
                    getCoresBg={getCoresBg}
                    getCorTexto={getCorTexto}
                    getLetraCor={getLetraCor}
                />

                {/* Seção de Compra de Bilhetes */}
                <SecaoCompraBilhetes game={game} />
            </div>
        </div>
    );
}

// Export padrão para compatibilidade
export default AcoesDoTurno;
