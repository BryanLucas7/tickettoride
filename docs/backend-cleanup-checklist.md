# Backend Cleanup Checklist

Use esta checklist para remover código legado e inconsistências identificadas no backend hexagonal. Execute os itens na ordem para evitar regressões.

## 1. Remover módulos/serviços não referenciados
- [ ] `app/interfaces/http/utils.py`: eliminar `processar_fim_acao` e apagar o módulo após verificar que nenhum roteador ou serviço mais depende dele.
- [ ] `app/core/domain/calculators/pontuacao_final.py` e `app/core/domain/calculators/pontuacao_final_service.py`: apagar ambos, mantendo apenas `app/services/pontuacao_final_service.py` como fluxo oficial.
- [ ] `app/core/domain/entities/game_manager.py`, `jogo_mock.py`, `acao_turno_base.py`, `acao_turno_concrete.py`, `acao_turno_types.py`: confirmar com `rg 'GameManager' -g '*.py' backend/app` (ou equivalente) e remover se não houver dependências reais.
- [ ] `app/core/domain/managers/compra_bilhetes_inicial.py` e `compra_bilhetes_service.py`: descontinuar em favor de `TicketSelectionService`/`TicketPurchaseService`.

## 2. Excluir funções legadas não chamadas
- [ ] `app/shared/validators.py::buscar_jogador_por_id_str`
- [ ] `app/core/domain/managers/compra_bilhetes_inicial.py::confirmar_escolha_inicial`
- [ ] Qualquer outra verificada com `rg -n "def .*" backend/app | xargs pyan` ou inspeção manual

## 3. Limpar imports não utilizados
Execute `pipx run pyflakes backend/app` após cada bloco para garantir limpeza.
- [ ] `app/adapters/inbound/http/routes/game_routes.py`: remover `HTTPException`, `Jogo`, `Jogador`, `Cor`, schemas extras, `logging`, `uuid`, `typing.*`, `get_validated_game`.
- [ ] `player_routes.py`, `route_routes.py`, `ticket_routes.py`: retirar services/dependencies herdados que agora vêm do `PlayerRequestContext`/`GameRequestContext` e `TicketSelectionService`.
- [ ] Schemas: `game_schemas.py` (remover `field_validator` não usado), `player_schemas.py` (remover `CorEnum`), `route_schemas.py` (remover `Field`).
- [ ] Serviços/utilidades: `ticket_purchase_service.py` (remover `HTTPException`), `game_creation_service.py` (remover `Dict`), `shared/request_context.py` (remover `Optional`), `shared/response_assembler.py` (remover `Rota`), `shared/validators.py` (remover `Tuple` e `GameService` do TYPE_CHECKING), `core/domain/calculators/pontuacao_final_types.py` (remover `Tuple`/`Optional`).
- [ ] `app/core/domain/entities/jogo_inicializador.py`: remover imports não utilizados (`GerenciadorDeTurnos`, `Tabuleiro`, `GerenciadorFimDeJogo`).

## 4. Resolver NameErrors pendentes
- [ ] Importar `DescarteManager` em `app/services/route_conquest_service.py` (o arquivo usa mas não importa).
- [ ] Garantir que arquivos que usam `Jogador`, `Jogo` ou `Rota` façam import explícito (ex.: `entities/rota.py`, `acao_turno_*`, `validador_rotas_duplas.py`).
- [ ] Reexecutar `pipx run pyflakes backend/app` até não restarem `undefined name`.

## 5. Validar fluxo de compra/conquista de bilhetes
- [ ] Após remover managers legados, revisar `TicketSelectionService` e `TicketPurchaseService` para garantir que não referenciam mais helpers apagados.
- [ ] Atualizar documentação em `docs/implementacao-helper-rotas-jogador.md` e `docs/implementacao-padronizacao-respostas-turno.md` se citarem métodos removidos.

## 6. Testar e registrar
- [ ] Executar `cd backend && pipx run pyflakes app` para confirmar lint limpo.
- [ ] Executar `cd backend && pytest` para garantir que a remoção não quebrou fluxos.
- [ ] Criar commit descrevendo: "chore: remove legacy backend artifacts".

> Dica: mantenha um branch separado para esta limpeza para facilitar rollback caso algum adaptador externo ainda dependa das APIs removidas.
