# backend/app/main.py

from fastapi import FastAPI
from .routers import convection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Convection API",
    description="API para cálculos de convección",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solo el origen específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(convection.router)