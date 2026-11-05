from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.initialization import ensure_patient_records, seed_initial_specialty, seed_test_users
from app.api.api_router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_initial_specialty(db)
        ensure_patient_records(db)
        if settings.SEED_TEST_USERS:
            seed_test_users(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs", # URL do Swagger UI
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Liberar CORS para integração com o Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "online", "system": "Prontuário Odontológico - Backend API"}
