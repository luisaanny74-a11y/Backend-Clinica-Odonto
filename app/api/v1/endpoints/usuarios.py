from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash
from domain.models import Usuario
from domain.enums import PerfilUsuario
from app.api.v1.schemas import UsuarioResponse, UsuarioCreate
from app.api.v1.dependencies import get_current_user, check_perfil

router = APIRouter()

@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(check_perfil([PerfilUsuario.ADMIN]))
):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    novo_usuario = Usuario(
        nome=data.nome,
        email=data.email,
        senha_hash=get_password_hash(data.senha),
        matricula=data.matricula,
        perfil=data.perfil
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario