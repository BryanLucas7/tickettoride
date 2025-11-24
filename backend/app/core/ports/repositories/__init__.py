"""
Repository Ports - Interfaces para persistência de dados

Define contratos para salvar/carregar dados do jogo.

Exemplo:
- JogoRepository: Interface para persistir jogos
  - salvar(jogo: Jogo) -> None
  - buscar(game_id: str) -> Optional[Jogo]
  - listar() -> List[Jogo]
  - deletar(game_id: str) -> None
"""
