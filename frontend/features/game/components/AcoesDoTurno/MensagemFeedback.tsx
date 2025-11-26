/**
 * Componente de mensagem de feedback
 * Exibe alertas e mensagens de feedback para o usuário
 */

import type { MensagemFeedbackProps } from './types';

/**
 * Mensagem de feedback com ícone de alerta
 */
export function MensagemFeedback({ mensagem, tipo = 'warning' }: MensagemFeedbackProps) {
    if (!mensagem) return null;

    const estilos = {
        warning: 'border-amber-200 bg-amber-50 text-amber-800',
        error: 'border-red-200 bg-red-50 text-red-800',
        info: 'border-blue-200 bg-blue-50 text-blue-800',
    };

    const icones = {
        warning: '⚠️',
        error: '❌',
        info: 'ℹ️',
    };

    return (
        <div className={`mt-3 flex items-start gap-2 rounded-md border p-2 text-xs ${estilos[tipo]}`}>
            <span className="text-base leading-none">{icones[tipo]}</span>
            <span>{mensagem}</span>
        </div>
    );
}
