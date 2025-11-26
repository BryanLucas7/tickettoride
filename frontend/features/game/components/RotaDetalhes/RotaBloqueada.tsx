/**
 * RotaBloqueada - Estado quando há ação em andamento que bloqueia interação
 * 
 * GRASP - High Cohesion: Focado em exibir mensagem de bloqueio
 */

import type { RotaBloqueadaProps } from './types'

const MENSAGENS = {
  cartas: "Conclua a compra de cartas antes de interagir com rotas.",
  bilhetes: "Conclua a compra de bilhetes antes de interagir com rotas."
} as const

export function RotaBloqueada({ motivo }: RotaBloqueadaProps) {
  return (
    <p className="text-sm text-orange-700 text-center">
      {MENSAGENS[motivo]}
    </p>
  )
}
