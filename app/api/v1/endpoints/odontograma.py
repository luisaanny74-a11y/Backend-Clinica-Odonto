from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from domain.models import Odontograma, OdontogramaRegistro, Atendimento, Usuario
from domain.enums import PerfilUsuario
from app.api.v1.schemas import OdontogramaRegistroCreate
from app.api.v1.dependencies import get_current_user, check_perfil

router = APIRouter()

@router.get("/prontuarios/{id}/odontograma")
def obter_odontograma(id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    odontograma = db.query(Odontograma).filter(Odontograma.prontuario_id == id).first()
    if not odontograma:
        raise HTTPException(status_code=404, detail="Odontograma não encontrado.")
    return odontograma

@router.post("/atendimentos/{atendimento_id}/odontograma/registros", status_code=status.HTTP_201_CREATED)
def registrar_condicao_odontograma(
    atendimento_id: int,
    data: OdontogramaRegistroCreate,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")
    if atendimento.aluno_id != aluno.id:
        raise HTTPException(status_code=403, detail="Não autorizado.")

    odontograma = db.query(Odontograma).filter(Odontograma.prontuario_id == atendimento.prontuario_id).first()
    if not odontograma:
        odontograma = Odontograma(prontuario_id=atendimento.prontuario_id)
        db.add(odontograma)
        db.flush()

    registro = OdontogramaRegistro(
        odontograma_id=odontograma.id,
        atendimento_id=atendimento_id,
        numero_dente=data.numero_dente,
        face=data.face,
        condicao_id=data.condicao_id,
        observacao=data.observacao,
        registrado_por=aluno.id
    )
    db.add(registro)
    db.commit()
    return {"message": "Registro de odontograma salvo."}