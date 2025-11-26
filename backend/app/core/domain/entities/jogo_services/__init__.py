"""
Internal Jogo Services - Serviços internos da entidade Jogo.

Estes serviços são "inner services" da entidade Jogo, seguindo o padrão
de delegação interna para reduzir a complexidade da classe principal.

NOTA ARQUITETURAL:
Estes serviços estão em `entities/` propositalmente porque:
1. São parte intrínseca da entidade Jogo (inner classes pattern)
2. Têm dependência bidirecional com Jogo (recebem `self.jogo`)
3. Não são serviços de aplicação independentes

Para serviços de aplicação externos (que orquestram múltiplas entidades),
use os serviços em `application/services/`:
- TicketPurchaseService
- RouteConquestService
- GameCreationService
- etc.

Exports:
- JogoInicializador: Configuração e inicialização do jogo
- JogoBilhetesService: Gerenciamento de bilhetes iniciais
- JogoComprasService: Operações de compra de cartas
- JogoActionsService: Ações gerais e validação de fim de jogo
"""

from .jogo_inicializador import JogoInicializador
from .jogo_bilhetes_service import JogoBilhetesService
from .jogo_compras_service import JogoComprasService
from .jogo_actions_service import JogoActionsService

__all__ = [
    'JogoInicializador',
    'JogoBilhetesService',
    'JogoComprasService',
    'JogoActionsService'
]
