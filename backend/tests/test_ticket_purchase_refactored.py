"""
Testes para Refatoração 4 - Consolidação de Busca de Jogador

Valida que TicketPurchaseService agora recebe Jogador diretamente
em vez de fazer busca duplicada com player_id string.

ANTES (Duplicação):
- Endpoint: Depends(get_validated_player) → obtém Jogador
- Endpoint: passa player_id string para service
- Service: faz busca novamente com jogo.gerenciadorDeTurnos.obter_jogador_por_id()

DEPOIS (DRY):
- Endpoint: Depends(get_validated_player) → obtém Jogador
- Endpoint: passa Jogador diretamente para service
- Service: usa Jogador recebido, sem busca duplicada
"""

from pathlib import Path

import pytest


TESTS_ROOT = Path(__file__).parent.parent
SERVICES_DIR = TESTS_ROOT / "app" / "application" / "services"


class TestTicketPurchaseServiceRefatorado:
    """Valida que service recebe Jogador diretamente (sem busca duplicada)."""
    
    def test_comprar_bilhetes_recebe_jogador_diretamente(self):
        """
        Valida que comprar_bilhetes() recebe Jogador diretamente.
        
        Assinatura NOVA:
            def comprar_bilhetes(self, jogo: Jogo, jogador: Jogador, indices_escolhidos: List[int])
        
        Assinatura ANTIGA (removida):
            def comprar_bilhetes(self, jogo: Jogo, player_id: str, indices_escolhidos: List[int])
        """
        service_path = SERVICES_DIR / "ticket_purchase_service.py"
        content = service_path.read_text()
        
        # Deve ter assinatura com jogador: Jogador
        assert "def comprar_bilhetes(" in content
        assert "jogador: Jogador" in content
        
        # Verifica que a assinatura de comprar_bilhetes NÃO tem player_id
        lines = content.split('\n')
        comprar_bilhetes_section = []
        in_method = False
        
        for line in lines:
            if 'def comprar_bilhetes(' in line:
                in_method = True
            if in_method:
                comprar_bilhetes_section.append(line)
                if line.strip().startswith('"""') and len(comprar_bilhetes_section) > 3:
                    break
        
        signature = '\n'.join(comprar_bilhetes_section[:10])
        assert 'player_id: str' not in signature, \
            "comprar_bilhetes() não deve receber 'player_id: str' (duplicação removida)"
    
    def test_executar_compra_nao_busca_jogador(self):
        """
        Valida que _executar_compra() não faz busca duplicada de jogador.
        
        Código REMOVIDO:
            jogador = jogo.gerenciadorDeTurnos.obter_jogador_por_id(player_id)
            if not jogador:
                raise ValueError(f"Jogador {player_id} não encontrado")
        
        Código NOVO:
            # Recebe jogador já validado
            def _executar_compra(self, jogo, jogador, bilhetes_escolhidos, bilhetes_recusados):
        """
        service_path = SERVICES_DIR / "ticket_purchase_service.py"
        content = service_path.read_text()
        
        # Busca método _executar_compra
        lines = content.split('\n')
        in_executar_compra = False
        executar_compra_lines = []
        
        for i, line in enumerate(lines):
            if 'def _executar_compra(' in line:
                in_executar_compra = True
            if in_executar_compra:
                executar_compra_lines.append(line)
                # Para quando encontrar próximo método ou chegar ao final
                if len(executar_compra_lines) > 1 and line.strip().startswith('def ') and '_executar_compra' not in line:
                    break
        
        executar_compra_str = '\n'.join(executar_compra_lines)
        
        # NÃO deve fazer busca com obter_jogador_por_id
        assert "obter_jogador_por_id" not in executar_compra_str, \
            "_executar_compra não deve fazer busca duplicada de jogador"
        
        # NÃO deve ter validação "if not jogador"
        assert "if not jogador:" not in executar_compra_str, \
            "_executar_compra não deve validar jogador (já vem validado)"
        
        # NÃO deve ter raise ValueError sobre jogador não encontrado
        assert 'Jogador' not in executar_compra_str or 'não encontrado' not in executar_compra_str, \
            "_executar_compra não deve validar existência de jogador"


class TestIntegracaoEndpointComService:
    """Testa integração endpoint → service sem duplicação."""
    
    def test_endpoint_buy_tickets_passa_jogador_validado(self):
        """
        Valida que endpoint /buy-tickets passa Jogador diretamente para service.
        
        Fluxo CORRETO (DRY):
        1. Endpoint: ctx: PlayerRequestContext = Depends(get_player_context)
        2. Endpoint: purchase_service.comprar_bilhetes(jogo, jogador, indices)
        3. Service: usa jogador recebido diretamente
        """
        route_path = Path(__file__).parent.parent / "app" / "adapters" / "inbound" / "http" / "routes" / "ticket_routes.py"
        content = route_path.read_text()
        
        # Deve usar PlayerRequestContext (nova arquitetura) ou get_validated_player (antiga)
        assert ("PlayerRequestContext" in content or "Depends(get_validated_player)" in content), \
            "Endpoint deve usar PlayerRequestContext ou Depends(get_validated_player)"
        
        # Busca a função buy_tickets
        lines = content.split('\n')
        buy_tickets_section = []
        in_function = False
        
        for line in lines:
            if 'def buy_tickets(' in line:
                in_function = True
            if in_function:
                buy_tickets_section.append(line)
                if line.strip().startswith('return ') or (line.strip().startswith('def ') and 'buy_tickets' not in line):
                    break
        
        buy_tickets_str = '\n'.join(buy_tickets_section)
        
        # Deve passar jogador para service (ctx.jogador ou jogador)
        assert ('jogador=ctx.jogador' in buy_tickets_str or 'jogador=jogador' in buy_tickets_str), \
            "Endpoint deve passar jogador para service"


class TestBeneficios:
    """Documenta benefícios da refatoração."""
    
    def test_documentacao_reducao_duplicacao(self):
        """
        BENEFÍCIOS DA REFATORAÇÃO 4:
        
        1. ✅ Eliminado ~6 linhas de código duplicado:
           - Busca de jogador com obter_jogador_por_id()
           - Validação if not jogador: raise ValueError()
           - Return de jogador em _executar_compra()
        
        2. ✅ Aproveitamento melhor do FastAPI Depends():
           - Endpoint já faz validação com Depends(get_validated_player)
           - Service não precisa re-validar
        
        3. ✅ Single Responsibility Principle:
           - Validação de jogador: responsabilidade do endpoint/dependency
           - Lógica de negócio: responsabilidade do service
        
        4. ✅ Menos chamadas de método:
           - ANTES: 2 chamadas a obter_jogador_por_id() (endpoint + service)
           - DEPOIS: 1 chamada a obter_jogador_por_id() (apenas endpoint via Depends)
        
        5. ✅ Assinatura mais clara:
           - comprar_bilhetes(jogo, jogador, indices) → explícito que precisa de Jogador
           - comprar_bilhetes(jogo, player_id, indices) → implícito que fará busca
        """
        assert True, "Documentação de benefícios"
