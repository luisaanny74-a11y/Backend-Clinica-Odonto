from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.core.database import get_db
from domain.models import Atendimento, Ficha, FichaSemiologia, Aprovacao, HistoricoStatusFicha, Usuario
from domain.enums import PerfilUsuario, StatusFicha
from app.api.v1.schemas import (
    FichaCreateResponse, FichaResponse, FichaSemiologiaBase,
    AprovacaoCreate
)
from app.api.v1.dependencies import get_current_user, check_perfil

router = APIRouter()

@router.post("/atendimentos/{id}/fichas/semiologia", response_model=FichaCreateResponse, status_code=status.HTTP_201_CREATED)
def criar_ficha_semiologia(
    id: int,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    atendimento = db.query(Atendimento).filter(Atendimento.id == id).first()
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")
    if atendimento.aluno_id != aluno.id:
        raise HTTPException(status_code=403, detail="Não autorizado a alterar este atendimento.")

    ficha = Ficha(atendimento_id=id, tipo="SEMIOLOGIA", status=StatusFicha.RASCUNHO)
    db.add(ficha)
    db.flush()

    semiologia = FichaSemiologia(ficha_id=ficha.id)
    db.add(semiologia)
    db.commit()

    return {
        "id": ficha.id,
        "atendimento_id": ficha.atendimento_id,
        "status": ficha.status,
        "versao": ficha.versao
    }

@router.get("/fichas/{id}", response_model=FichaResponse)
def obter_ficha(id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    ficha = db.query(Ficha).filter(Ficha.id == id).first()
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada.")
    return ficha

@router.patch("/fichas/{id}", response_model=FichaResponse)
def salvar_rascunho(
    id: int,
    data: FichaSemiologiaBase,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    ficha = db.query(Ficha).filter(Ficha.id == id).first()
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada.")
    if ficha.atendimento.aluno_id != aluno.id:
        raise HTTPException(status_code=403, detail="Apenas o aluno responsável pode editar a ficha.")
    if ficha.status not in [StatusFicha.RASCUNHO, StatusFicha.CORRECAO_SOLICITADA]:
        raise HTTPException(status_code=400, detail="Ficha bloqueada para edição no status atual.")

    semiologia = db.query(FichaSemiologia).filter(FichaSemiologia.ficha_id == id).first()
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(semiologia, key, value)

    db.commit()
    db.refresh(ficha)
    return ficha

@router.patch("/fichas/{id}/submeter")
def submeter_ficha(
    id: int,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    ficha = db.query(Ficha).filter(Ficha.id == id).first()
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada.")
    if ficha.atendimento.aluno_id != aluno.id:
        raise HTTPException(status_code=403, detail="Operação negada.")
    if ficha.status not in [StatusFicha.RASCUNHO, StatusFicha.CORRECAO_SOLICITADA]:
        raise HTTPException(status_code=400, detail="Apenas rascunhos ou fichas em correção podem ser submetidos.")

    status_anterior = ficha.status.value
    ficha.status = StatusFicha.AGUARDANDO_APROVACAO
    ficha.enviada_em = datetime.utcnow()

    # Rastreabilidade em HistoricoStatusFicha
    historico = HistoricoStatusFicha(
        ficha_id=ficha.id,
        status_anterior=status_anterior,
        status_novo=ficha.status.value,
        usuario_id=aluno.id
    )
    db.add(historico)
    db.commit()

    return {"id": ficha.id, "status": ficha.status}

@router.get("/fichas", response_model=List[FichaResponse])
def listar_fichas_professores(
    status: Optional[StatusFicha] = Query(None),
    db: Session = Depends(get_db),
    professor: Usuario = Depends(check_perfil([PerfilUsuario.PROFESSOR]))
):
    query = db.query(Ficha)
    if status:
        query = query.filter(Ficha.status == status)
    return query.all()

@router.post("/fichas/{id}/aprovacoes")
def registrar_decisao(
    id: int,
    data: AprovacaoCreate,
    db: Session = Depends(get_db),
    professor: Usuario = Depends(check_perfil([PerfilUsuario.PROFESSOR]))
):
    ficha = db.query(Ficha).filter(Ficha.id == id).first()
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada.")
    if ficha.status != StatusFicha.AGUARDANDO_APROVACAO:
        raise HTTPException(status_code=400, detail="Esta ficha não está aguardando revisão.")

    status_anterior = ficha.status.value
    novo_status = StatusFicha.APROVADA if data.decisao == StatusFicha.APROVADA else StatusFicha.CORRECAO_SOLICITADA

    ficha.status = novo_status
    if novo_status == StatusFicha.APROVADA:
        ficha.aprovada_em = datetime.utcnow()

    aprovacao = Aprovacao(
        ficha_id=id,
        professor_id=professor.id,
        decisao=data.decisao,
        observacao=data.observacao
    )
    db.add(aprovacao)

    historico = HistoricoStatusFicha(
        ficha_id=id,
        status_anterior=status_anterior,
        status_novo=novo_status.value,
        usuario_id=professor.id
    )
    db.add(historico)

    db.commit()
    return {"message": "Decisão registrada com sucesso.", "novo_status": novo_status}