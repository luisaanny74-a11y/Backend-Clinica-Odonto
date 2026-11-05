from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from domain.models import Usuario
from app.api.v1.schemas import LoginSchema, TokenResponse, UsuarioResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user or not verify_password(data.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciais inválidas."
        )
    if not user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo.")

    # PyJWT 2.10+ validates that the standard JWT `sub` claim is a string.
    token = create_access_token({"sub": str(user.id), "perfil": user.perfil.value})
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": user
    }
