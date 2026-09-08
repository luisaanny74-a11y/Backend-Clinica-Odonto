from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from domain.models import Atendimento, SinaisVitais, Usuario
from domain.enums import PerfilUsuario
from app.api.v1.schemas import AtendimentoCreate, AtendimentoResponse, SinaisVitaisCreate
from app.api.v1.dependencies import get_current_user, check_perfil

router = APIRouter()

@router.post("", response_model=AtendimentoResponse, status_code=status.HTTP_201_CREATED)
def criar_atendimento(
    data: AtendimentoCreate,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    atendimento = Atendimento(
        prontuario_id=data.prontuario_id,
        especialidade_id=data.especialidade_id,
        aluno_id=aluno.id
    )
    db.add(atendimento)
    db.commit()
    db.refresh(atendimento)
    return atendimento

@router.get("/meus", response_model=List[AtendimentoResponse])
def meus_atendimentos(
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    return db.query(Atendimento).filter(Atendimento.aluno_id == aluno.id).all()

@router.post("/{id}/sinais-vitais", status_code=status.HTTP_201_CREATED)
def registrar_sinais_vitais(
    id: int,
    data: SinaisVitaisCreate,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    atendimento = db.query(Atendimento).filter(Atendimento.id == id).first()
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")
    if atendimento.aluno_id != aluno.id:
        raise HTTPException(status_code=403, detail="Apenas o aluno responsável pode registrar os sinais vitais.")

    sv = SinaisVitais(
        atendimento_id=id,
        registrado_por=aluno.id,
        **data.model_dump()
    )
    db.add(sv)
    db.commit()
    return {"message": "Sinais vitais gravados com sucesso."}