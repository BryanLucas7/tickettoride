"""
API FastAPI para Ticket to Ride - Arquitetura Hexagonal

Ponto de entrada da aplicação que:
1. Configura FastAPI e middleware
2. Injeta dependências (Repository)
3. Registra routers

Arquitetura Hexagonal:
- API é um thin layer que delega para services
- Routes (adapters inbound) usam services
- Services usam repositories (adapters outbound)
- Core não depende de frameworks
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Importa repository para dependency injection
from .dependencies.repositories import get_jogo_repository as di_get_jogo_repository
from .dependencies.services import get_game_service as di_get_game_service

# Importa routes
from .adapters.inbound.http.routes import game_routes, player_routes, ticket_routes, route_routes, map_routes


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Dependency Injection - Singleton instances
# Repository implementation (pode trocar PickleJogoRepository por SQLJogoRepository sem mudar nada)
jogo_repository = di_get_jogo_repository()

# Service layer (usa o repository)
game_service = di_get_game_service(jogo_repository)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia lifecycle da aplicação.
    
    Startup: Carrega jogos do repository
    Shutdown: Não precisa fazer nada (repository já persiste automaticamente)
    """
    logger.info("🚀 Iniciando Ticket to Ride API")
    logger.info(f"📦 Jogos carregados: {len(jogo_repository.listar())}")
    
    yield
    
    logger.info("👋 Encerrando Ticket to Ride API")


# Cria aplicação FastAPI
app = FastAPI(
    title="Ticket to Ride API",
    description="API RESTful para o jogo Ticket to Ride - Arquitetura Hexagonal",
    version="2.0.0",
    lifespan=lifespan
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Ticket to Ride API",
        "status": "running",
        "version": "2.0.0",
        "architecture": "Hexagonal (Ports & Adapters)",
        "active_games": len(jogo_repository.listar())
    }


# Registra routers
app.include_router(game_routes.router, prefix="/games", tags=["Games"])
app.include_router(player_routes.router, prefix="/games", tags=["Players"])
app.include_router(ticket_routes.router, prefix="/games", tags=["Tickets"])
app.include_router(route_routes.router, prefix="/games", tags=["Routes"])
app.include_router(map_routes.router, prefix="/map", tags=["Map"])


# Disponibiliza services para injeção de dependência nas routes
def get_jogo_repository():
    """Fornece instância do repository para dependency injection."""
    return jogo_repository


def get_game_service():
    """Fornece instância do GameService para dependency injection."""
    return game_service


logger.info("✅ API configurada com sucesso")
