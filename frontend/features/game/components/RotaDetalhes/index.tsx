/**
 * RotaDetalhesPanel - Painel de detalhes da rota selecionada (REFATORADO)
 * 
 * Princípios GRASP aplicados:
 * - SRP: Subcomponentes extraídos para cada estado
 * - Low Coupling: Estados isolados em componentes independentes
 * - High Cohesion: Cada componente focado em um único estado
 * 
 * Refatoração: 129 linhas → ~60 linhas (orquestrador)
 * 
 * Estados possíveis:
 * - RotaConquistada: Rota já pertence a outro jogador
 * - RotaBloqueada: Fluxo de cartas/bilhetes em andamento
 * - RotaAguardando: Não é a vez do jogador
 * - RotaSemCartas: Jogador sem cartas disponíveis
 * - RotaSelecaoCartas: Seleção ativa para conquista
 */

import { RotaConquistada } from './RotaConquistada'
import { RotaBloqueada } from './RotaBloqueada'
import { RotaAguardando } from './RotaAguardando'
import { RotaSemCartas } from './RotaSemCartas'
import { RotaSelecaoCartas } from './RotaSelecaoCartas'
import type { RotaDetalhesPanelProps } from './types'

// Re-exportar tipos
export type { RotaDetalhesPanelProps } from './types'

/**
 * Componente orquestrador que delega para o subcomponente apropriado
 * baseado no estado atual do jogo
 * 
 * NOTA: getCoresBg, getCorTexto, getLetraCor são mantidos por compatibilidade
 * mas não são mais usados (CardSelectionGrid usa useCardColors internamente)
 */
export function RotaDetalhesPanel({
  rotaMapa,
  rotaDoJogo,
  game,
  ehMinhaVez,
  // Props de cores mantidas por compatibilidade (não usadas - useCardColors é usado internamente)
  getCoresBg: _getCoresBg,
  getCorTexto: _getCorTexto,
  getLetraCor: _getLetraCor
}: RotaDetalhesPanelProps) {
  // Estado 1: Rota já conquistada
  if (rotaDoJogo?.conquistada) {
    return <RotaConquistada proprietarioNome={rotaDoJogo.proprietario_nome} />
  }

  // Estado 2: Ação bloqueando interação
  if (game.acaoCartasBloqueiaOutras) {
    return <RotaBloqueada motivo="cartas" />
  }
  
  if (game.fluxoBilhetesAtivo || game.carregandoBilhetesPreview) {
    return <RotaBloqueada motivo="bilhetes" />
  }

  // Estado 3: Não é minha vez
  if (!ehMinhaVez) {
    return <RotaAguardando />
  }

  // Estado 4: Sem cartas disponíveis
  if (game.minhasCartas.length === 0) {
    return <RotaSemCartas />
  }

  // Estado 5: Seleção ativa de cartas
  // CardSelectionGrid usa useCardColors internamente - não precisa de props de cores
  return (
    <RotaSelecaoCartas
      rotaMapa={rotaMapa}
      game={game}
    />
  )
}

// Export padrão para compatibilidade
export default RotaDetalhesPanel
