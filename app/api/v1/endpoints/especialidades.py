from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user
from app.api.v1.schemas import EspecialidadeResponse
from app.core.database import get_db
from domain.models import Especialidade, Usuario

router = APIRouter()


@router.get("", response_model=List[EspecialidadeResponse])
def listar_especialidades(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    return db.query(Especialidade).order_by(Especialidade.id).all()
