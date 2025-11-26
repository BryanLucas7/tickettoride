/**
 * Barrel export para componentes e tipos compartilhados
 * 
 * REFATORAÇÃO DRY: Componentes extraídos de múltiplos lugares
 */
export * from './types'
export { 
  CardSelectionGrid, 
  SelectionInstructions,
  type CardSelectionGridProps,
  type SelectionInstructionsProps 
} from './CardSelectionGrid'
