"""
API FastAPI para Ticket to Ride

Implementa os endpoints RESTful para o jogo.

Princípios GRASP aplicados:
- Controller: API endpoints coordenam as ações do jogo
- Pure Fabrication: Schemas Pydantic para camada de API
- Low Coupling: API separada da lógica de domínio
- Indirection: API serve como intermediário entre frontend e backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .routes.game_routes