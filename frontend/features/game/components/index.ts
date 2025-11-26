/**
 * Barrel export para componentes do jogo
 */

// Componentes com estrutura de pasta (refatorados SRP)
export { default as Board } from "./Board"
export { ContadorTrens } from "./ContadorTrens"
export { default as MaoCartas } from "./MaoCartas"
export { default as PainelBilhetesDestino } from "./PainelBilhetesDestino"
export { default as TelaFimJogo } from "./TelaFimJogo"
export { TrilhaPontuacao } from "./TrilhaPontuacao"
export { AcoesDoTurno } from "./AcoesDoTurno"
export { RotaDetalhesPanel } from "./RotaDetalhes"

// Componentes simples (arquivo único)
export { GameHeader } from "./GameHeader"
export { ListaJogadores } from "./ListaJogadores"
export { MaiorCaminhoWidget } from "./MaiorCaminhoWidget"
export { ModalBilhetes } from "./ModalBilhetes"
export { MinhasCartasPanel } from "./MinhasCartasPanel"
export { RotasConquistadasPanel } from "./RotasConquistadasPanel"

