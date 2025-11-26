/**
 * RotaSemCartas - Estado quando jogador não tem cartas disponíveis
 * 
 * GRASP - High Cohesion: Focado em exibir mensagem de falta de cartas
 */

export function RotaSemCartas() {
  return (
    <p className="text-sm text-gray-600 text-center">
      Você não tem cartas disponíveis. Compre cartas para poder conquistar rotas.
    </p>
  )
}
