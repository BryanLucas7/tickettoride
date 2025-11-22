/**
 * STATE PATTERN - Controle de Estado do Turno
 * ============================================
 * 
 * Padrão GoF: State Pattern
 * - Permite que objeto altere comportamento quando estado interno muda
 * - Objeto parece mudar de classe
 * 
 * Estados do Turno:
 * - AguardandoAcaoState: Jogador pode escolher uma das 3 ações
 * - AcaoEmAndamentoState: Ação sendo executada, aguardando conclusão
 * - AcaoConcluidaState: Ação concluída, aguardando próximo turno
 * 
 * GRASP Principles:
 * - Controller: TurnoContext coordena transições de estado
 * - High Cohesion: Cada estado focado em comportamento específico
 * - Polymorphism: Comportamento muda baseado no estado
 * - Protected Variations: Estados encapsulam variações de comportamento
 */

export enum AcaoTurno {
    COMPRAR_CARTAS = 'COMPRAR_CARTAS',
    CONQUISTAR_ROTA = 'CONQUISTAR_ROTA',
    COMPRAR_BILHETES = 'COMPRAR_BILHETES'
}

export interface TurnoStateResult {
    sucesso: boolean;
    mensagem: string;
    dados?: any;
}

/**
 * Interface base do State Pattern
 * Define contrato que todos os estados devem seguir
 */
export interface TurnoState {
    /**
     * Verifica se ação está disponível no estado atual
     */
    podeExecutarAcao(acao: AcaoTurno): boolean;
    
    /**
     * Executa ação no estado atual
     */
    executarAcao(acao: AcaoTurno, context: TurnoContext): TurnoStateResult;
    
    /**
     * Finaliza estado atual
     */
    finalizarEstado(context: TurnoContext): void;
    
    /**
     * Retorna nome do estado
     */
    getNomeEstado(): string;
    
    /**
     * Retorna ações disponíveis no estado
     */
    getAcoesDisponiveis(): AcaoTurno[];
}

/**
 * Estado 1: Aguardando Ação
 * Jogador pode escolher qualquer uma das 3 ações
 */
export class AguardandoAcaoState implements TurnoState {
    podeExecutarAcao(acao: AcaoTurno): boolean {
        // Todas as ações estão disponíveis
        return true;
    }
    
    executarAcao(acao: AcaoTurno, context: TurnoContext): TurnoStateResult {
        // Armazena ação escolhida
        context.setAcaoEscolhida(acao);
        
        // Transição para AcaoEmAndamentoState
        context.setState(new AcaoEmAndamentoState(acao));
        
        return {
            sucesso: true,
            mensagem: `Ação ${acao} iniciada`,
            dados: { acaoIniciada: acao }
        };
    }
    
    finalizarEstado(context: TurnoContext): void {
        // Nada a fazer ao sair deste estado
    }
    
    getNomeEstado(): string {
        return 'AguardandoAcao';
    }
    
    getAcoesDisponiveis(): AcaoTurno[] {
        return [
            AcaoTurno.COMPRAR_CARTAS,
            AcaoTurno.CONQUISTAR_ROTA,
            AcaoTurno.COMPRAR_BILHETES
        ];
    }
}

/**
 * Estado 2: Ação Em Andamento
 * Aguardando conclusão da ação escolhida
 */
export class AcaoEmAndamentoState implements TurnoState {
    private acaoAtual: AcaoTurno;
    
    constructor(acao: AcaoTurno) {
        this.acaoAtual = acao;
    }
    
    podeExecutarAcao(acao: AcaoTurno): boolean {
        // Nenhuma outra ação pode ser executada
        return false;
    }
    
    executarAcao(acao: AcaoTurno, context: TurnoContext): TurnoStateResult {
        return {
            sucesso: false,
            mensagem: `Ação ${this.acaoAtual} em andamento. Complete antes de escolher outra.`
        };
    }
    
    finalizarEstado(context: TurnoContext): void {
        // Transição para AcaoConcluidaState
        context.setState(new AcaoConcluidaState(this.acaoAtual));
    }
    
    getNomeEstado(): string {
        return 'AcaoEmAndamento';
    }
    
    getAcoesDisponiveis(): AcaoTurno[] {
        return []; // Nenhuma ação disponível
    }
    
    getAcaoAtual(): AcaoTurno {
        return this.acaoAtual;
    }
}

/**
 * Estado 3: Ação Concluída
 * Aguardando próximo turno
 */
export class AcaoConcluidaState implements TurnoState {
    private acaoConcluida: AcaoTurno;
    
    constructor(acao: AcaoTurno) {
        this.acaoConcluida = acao;
    }
    
    podeExecutarAcao(acao: AcaoTurno): boolean {
        // Turno já concluído, nenhuma ação disponível
        return false;
    }
    
    executarAcao(acao: AcaoTurno, context: TurnoContext): TurnoStateResult {
        return {
            sucesso: false,
            mensagem: 'Turno já concluído. Aguarde o próximo turno.'
        };
    }
    
    finalizarEstado(context: TurnoContext): void {
        // Limpa dados do turno anterior
        context.setAcaoEscolhida(null);
    }
    
    getNomeEstado(): string {
        return 'AcaoConcluida';
    }
    
    getAcoesDisponiveis(): AcaoTurno[] {
        return []; // Nenhuma ação disponível
    }
    
    getAcaoConcluida(): AcaoTurno {
        return this.acaoConcluida;
    }
}

/**
 * Context do State Pattern
 * Mantém referência ao estado atual e coordena transições
 * 
 * GRASP Controller: Coordena mudanças de estado do turno
 */
export class TurnoContext {
    private state: TurnoState;
    private acaoEscolhida: AcaoTurno | null = null;
    private jogadorId: string;
    private callbacks: {
        onStateChange?: (novoEstado: string) => void;
        onAcaoIniciada?: (acao: AcaoTurno) => void;
        onAcaoConcluida?: (acao: AcaoTurno) => void;
    } = {};
    
    constructor(jogadorId: string) {
        this.jogadorId = jogadorId;
        this.state = new AguardandoAcaoState();
    }
    
    /**
     * Altera estado atual
     * Protected Variations: Encapsula transições de estado
     */
    setState(novoEstado: TurnoState): void {
        const estadoAnterior = this.state.getNomeEstado();
        
        // Finaliza estado anterior
        this.state.finalizarEstado(this);
        
        // Define novo estado
        this.state = novoEstado;
        
        console.log(`[TurnoContext] Transição: ${estadoAnterior} → ${novoEstado.getNomeEstado()}`);
        
        // Notifica callback
        if (this.callbacks.onStateChange) {
            this.callbacks.onStateChange(novoEstado.getNomeEstado());
        }
    }
    
    /**
     * Tenta executar ação no estado atual
     * Polymorphism: Comportamento delegado ao estado
     */
    executarAcao(acao: AcaoTurno): TurnoStateResult {
        console.log(`[TurnoContext] Tentando executar: ${acao} no estado ${this.state.getNomeEstado()}`);
        
        if (!this.state.podeExecutarAcao(acao)) {
            return {
                sucesso: false,
                mensagem: `Ação ${acao} não disponível no estado ${this.state.getNomeEstado()}`
            };
        }
        
        const resultado = this.state.executarAcao(acao, this);
        
        if (resultado.sucesso && this.callbacks.onAcaoIniciada) {
            this.callbacks.onAcaoIniciada(acao);
        }
        
        return resultado;
    }
    
    /**
     * Conclui ação em andamento
     */
    concluirAcao(): TurnoStateResult {
        if (!(this.state instanceof AcaoEmAndamentoState)) {
            return {
                sucesso: false,
                mensagem: 'Nenhuma ação em andamento para concluir'
            };
        }
        
        const acaoAtual = (this.state as AcaoEmAndamentoState).getAcaoAtual();
        
        // Finaliza estado (transiciona para AcaoConcluida)
        this.state.finalizarEstado(this);
        
        if (this.callbacks.onAcaoConcluida) {
            this.callbacks.onAcaoConcluida(acaoAtual);
        }
        
        return {
            sucesso: true,
            mensagem: `Ação ${acaoAtual} concluída`,
            dados: { acaoConcluida: acaoAtual }
        };
    }
    
    /**
     * Inicia novo turno
     */
    iniciarNovoTurno(): void {
        console.log('[TurnoContext] Iniciando novo turno');
        
        // Retorna ao estado inicial
        this.setState(new AguardandoAcaoState());
    }
    
    /**
     * Verifica se ação está disponível
     */
    podeExecutarAcao(acao: AcaoTurno): boolean {
        return this.state.podeExecutarAcao(acao);
    }
    
    /**
     * Retorna ações disponíveis no estado atual
     */
    getAcoesDisponiveis(): AcaoTurno[] {
        return this.state.getAcoesDisponiveis();
    }
    
    /**
     * Retorna estado atual
     */
    getEstadoAtual(): string {
        return this.state.getNomeEstado();
    }
    
    /**
     * Retorna ação escolhida (se houver)
     */
    getAcaoEscolhida(): AcaoTurno | null {
        return this.acaoEscolhida;
    }
    
    /**
     * Define ação escolhida
     */
    setAcaoEscolhida(acao: AcaoTurno | null): void {
        this.acaoEscolhida = acao;
    }
    
    /**
     * Registra callbacks para eventos
     */
    setCallbacks(callbacks: {
        onStateChange?: (novoEstado: string) => void;
        onAcaoIniciada?: (acao: AcaoTurno) => void;
        onAcaoConcluida?: (acao: AcaoTurno) => void;
    }): void {
        this.callbacks = callbacks;
    }
    
    /**
     * Retorna ID do jogador
     */
    getJogadorId(): string {
        return this.jogadorId;
    }
}
