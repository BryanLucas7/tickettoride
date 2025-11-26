/**
 * RotaConquistada - Estado quando a rota já foi conquistada
 * 
 * GRASP - High Cohesion: Focado apenas em exibir estado de rota conquistada
 */

import type { RotaConquistadaProps } from './types'

export function RotaConquistada({ proprietarioNome }: RotaConquistadaProps) {
  return (
    <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-sm text-green-800">
      Essa rota já foi conquistada por {proprietarioNome || 'outro jogador'}.
    </div>
  )
}
