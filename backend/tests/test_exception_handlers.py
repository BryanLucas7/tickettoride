"""
Testes para Refatoração 5 - Decorator de Exception Handling

Valida que o decorator @handle_validation_errors elimina código duplicado
de try/except em services e endpoints.

ANTES (Duplicação em ~10+ lugares):
    try:
        resultado = alguma_operacao()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

DEPOIS (Centralizado):
    @handle_validation_errors
    def alguma_operacao():
        ...
"""

from pathlib import Path

import pytest
from fastapi import HTTPException
from backend.app.shared.exception_handlers import handle_validation_errors


TESTS_ROOT = Path(__file__).parent.parent
SERVICES_DIR = TESTS_ROOT / "app" / "application" / "services"


class TestHandleValidationErrors:
    """Testa o decorator @handle_validation_errors."""
    
    def test_decorator_converte_value_error_em_http_exception(self):
        """Decorator deve converter ValueError em HTTPException(400)."""
        @handle_validation_errors
        def funcao_que_levanta_value_error():
            raise ValueError("Erro de validação")
        
        with pytest.raises(HTTPException) as exc_info:
            funcao_que_levanta_value_error()
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Erro de validação"
    
    def test_decorator_preserva_http_exception(self):
        """Decorator deve re-raise HTTPException sem modificar."""
        @handle_validation_errors
        def funcao_que_levanta_http_exception():
            raise HTTPException(status_code=404, detail="Not found")
        
        with pytest.raises(HTTPException) as exc_info:
            funcao_que_levanta_http_exception()
        
        # Deve preservar status code e detail originais
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Not found"
    
    def test_decorator_nao_afeta_retorno_normal(self):
        """Decorator não deve afetar funções que retornam normalmente."""
        @handle_validation_errors
        def funcao_normal():
            return {"resultado": "sucesso"}
        
        resultado = funcao_normal()
        assert resultado == {"resultado": "sucesso"}
    
    def test_decorator_propaga_outras_excecoes(self):
        """Outras exceções devem propagar normalmente."""
        @handle_validation_errors
        def funcao_que_levanta_runtime_error():
            raise RuntimeError("Erro inesperado")
        
        with pytest.raises(RuntimeError) as exc_info:
            funcao_que_levanta_runtime_error()
        
        assert str(exc_info.value) == "Erro inesperado"
    
    def test_decorator_com_argumentos(self):
        """Decorator deve funcionar com funções que recebem argumentos."""
        @handle_validation_errors
        def validar_idade(idade: int):
            if idade < 0:
                raise ValueError("Idade não pode ser negativa")
            return idade
        
        # Caso válido
        assert validar_idade(25) == 25
        
        # Caso inválido
        with pytest.raises(HTTPException) as exc_info:
            validar_idade(-5)
        
        assert exc_info.value.status_code == 400
        assert "negativa" in exc_info.value.detail


class TestIntegracaoComServices:
    """Testa integração do decorator com services reais."""
    
    def test_ticket_purchase_service_usa_decorator(self):
        """TicketPurchaseService.comprar_bilhetes deve usar decorator."""
        service_path = SERVICES_DIR / "ticket_purchase_service.py"
        content = service_path.read_text()
        
        # Deve importar o decorator
        assert "from ...shared.exception_handlers import handle_validation_errors" in content
        
        # Deve ter decorator antes de comprar_bilhetes
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def comprar_bilhetes(' in line:
                # Linha anterior deve ter o decorator
                prev_line = lines[i-1].strip()
                assert '@handle_validation_errors' in prev_line, \
                    "comprar_bilhetes deve ter decorator @handle_validation_errors"
                break
    
    def test_route_conquest_service_usa_decorator(self):
        """RouteConquestService.conquistar_rota deve usar decorator."""
        service_path = SERVICES_DIR / "route_conquest_service.py"
        content = service_path.read_text()
        
        # Deve importar o decorator
        assert "from ...shared.exception_handlers import handle_validation_errors" in content
        
        # Deve ter decorator antes de conquistar_rota
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def conquistar_rota(' in line:
                # Linha anterior deve ter o decorator
                prev_line = lines[i-1].strip()
                assert '@handle_validation_errors' in prev_line, \
                    "conquistar_rota deve ter decorator @handle_validation_errors"
                break
    
    def test_services_nao_tem_mais_try_except_manual(self):
        """Services não devem ter try/except ValueError manual."""
        # TicketPurchaseService
        service_path = SERVICES_DIR / "ticket_purchase_service.py"
        content = service_path.read_text()
        
        # Busca método comprar_bilhetes
        lines = content.split('\n')
        in_comprar_bilhetes = False
        comprar_bilhetes_content = []
        
        for line in lines:
            if 'def comprar_bilhetes(' in line:
                in_comprar_bilhetes = True
            if in_comprar_bilhetes:
                comprar_bilhetes_content.append(line)
                if line.strip().startswith('def ') and 'comprar_bilhetes' not in line:
                    break
        
        method_str = '\n'.join(comprar_bilhetes_content)
        
        # NÃO deve ter try/except manual
        assert 'except ValueError' not in method_str, \
            "comprar_bilhetes não deve ter try/except manual (decorator faz isso)"
        assert 'except HTTPException' not in method_str, \
            "comprar_bilhetes não deve ter try/except manual (decorator faz isso)"


class TestIntegracaoComEndpoints:
    """Testa integração do decorator com endpoints."""
    
    def test_buy_tickets_endpoint_usa_decorator(self):
        """Endpoint buy_tickets deve usar decorator."""
        from pathlib import Path
        
        route_path = Path(__file__).parent.parent / "app" / "adapters" / "inbound" / "http" / "routes" / "ticket_routes.py"
        content = route_path.read_text()
        
        # Deve importar o decorator
        assert "from .....shared.exception_handlers import handle_validation_errors" in content
        
        # Deve ter decorator antes de buy_tickets
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def buy_tickets(' in line:
                # Deve ter decorator nas linhas anteriores (pode ter @router também)
                previous_lines = '\n'.join(lines[max(0, i-3):i])
                assert '@handle_validation_errors' in previous_lines, \
                    "buy_tickets deve ter decorator @handle_validation_errors"
                break
    
    def test_endpoint_nao_tem_try_except_manual(self):
        """Endpoint buy_tickets não deve ter try/except manual."""
        from pathlib import Path
        
        route_path = Path(__file__).parent.parent / "app" / "adapters" / "inbound" / "http" / "routes" / "ticket_routes.py"
        content = route_path.read_text()
        
        # Busca função buy_tickets
        lines = content.split('\n')
        in_buy_tickets = False
        buy_tickets_content = []
        
        for line in lines:
            if 'def buy_tickets(' in line:
                in_buy_tickets = True
            if in_buy_tickets:
                buy_tickets_content.append(line)
                if line.strip().startswith('def ') and 'buy_tickets' not in line:
                    break
                if line.strip().startswith('return '):
                    break
        
        function_str = '\n'.join(buy_tickets_content)
        
        # NÃO deve ter try/except manual
        assert 'except ValueError' not in function_str, \
            "buy_tickets não deve ter try/except manual (decorator faz isso)"


class TestBeneficios:
    """Documenta benefícios da refatoração."""
    
    def test_documentacao_reducao_duplicacao(self):
        """
        BENEFÍCIOS DA REFATORAÇÃO 5:
        
        1. ✅ Eliminado ~30 linhas de código duplicado:
           - try/except ValueError → HTTPException(400) em múltiplos lugares
           - try/except HTTPException → re-raise em múltiplos lugares
        
        2. ✅ Tratamento de exceções centralizado:
           - Um único lugar para modificar comportamento
           - Consistência em toda a aplicação
        
        3. ✅ Código mais limpo e legível:
           - Métodos focam na lógica de negócio
           - Não poluídos com try/except repetitivos
        
        4. ✅ Facilita manutenção:
           - Adicionar novo tipo de exceção: modificar apenas o decorator
           - Mudar status code: modificar apenas o decorator
        
        5. ✅ Testabilidade:
           - Decorator testado isoladamente
           - Services testam apenas lógica de negócio
        
        6. ✅ Decorator reutilizável:
           - Pode ser aplicado em qualquer service ou endpoint
           - Versão sync e async disponíveis
        """
        assert True, "Documentação de benefícios"
