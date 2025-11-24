"""
Ports - Interfaces para comunicação com o mundo externo

Define contratos (interfaces) que os adapters devem implementar.

Tipos de Ports:
- Inbound Ports: Interfaces chamadas pelo mundo externo (ex: HTTP handlers)
- Outbound Ports: Interfaces para chamar o mundo externo (ex: repositories)

Princípio de Inversão de Dependência:
Core define as interfaces, adapters as implementam.
"""
