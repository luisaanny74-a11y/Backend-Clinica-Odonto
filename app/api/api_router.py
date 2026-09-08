from fastapi import APIRouter
from app.api.v1.endpoints import auth, usuarios, pacientes, atendimentos, fichas, odontograma

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(pacientes.router, prefix="/pacientes", tags=["Pacientes"])
api_router.include_router(atendimentos.router, prefix="/atendimentos", tags=["Atendimentos"])
api_router.include_router(fichas.router, tags=["Fichas & Semiologia"])
api_router.include_router(odontograma.router, tags=["Odontograma"])