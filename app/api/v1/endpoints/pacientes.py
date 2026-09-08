from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from domain.models import Paciente, Prontuario, Alergia, PacienteCondicaoMedica, MedicamentoPaciente, Usuario
from domain.enums import PerfilUsuario
from app.api.v1.schemas import (
    PacienteCreate, PacienteCreateResponse, PacienteResponse,
    AlergiaCreate, CondicaoMedicaCreate, MedicamentoCreate
)
from app.api.v1.dependencies import get_current_user, check_perfil

router = APIRouter()

@router.get("", response_model=List[PacienteResponse])
def listar_pacientes(
    busca: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    query = db.query(Paciente)
    if cpf:
        query = query.filter(Paciente.cpf == cpf)
    elif busca:
        query = query.filter(Paciente.nome_completo.ilike(f"%{busca}%"))
    return query.all()

@router.post("", response_model=PacienteCreateResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_paciente(
    data: PacienteCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO, PerfilUsuario.ADMIN]))
):
    if data.cpf and db.query(Paciente).filter(Paciente.cpf == data.cpf).first():
        raise HTTPException(status_code=409, detail="CPF já cadastrado no sistema.")

    paciente = Paciente(**data.model_dump())
    db.add(paciente)
    db.flush()

    # Criação Automática do Prontuário 1:1 (Regra Requisitos / DDL)
    prontuario = Prontuario(paciente_id=paciente.id)
    db.add(prontuario)
    db.commit()

    return {
        "paciente_id": paciente.id,
        "prontuario_id": prontuario.id,
        "nome_completo": paciente.nome_completo
    }

@router.get("/{id}", response_model=PacienteResponse)
def obter_paciente(id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    return paciente

@router.post("/{id}/alergias", status_code=status.HTTP_201_CREATED)
def adicionar_alergia(
    id: int,
    data: AlergiaCreate,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    alergia = Alergia(paciente_id=id, **data.model_dump())
    db.add(alergia)
    db.commit()
    return {"message": "Alergia registrada com sucesso."}

@router.post("/{id}/condicoes-medicas", status_code=status.HTTP_201_CREATED)
def adicionar_condicao(
    id: int,
    data: CondicaoMedicaCreate,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    pcm = PacienteCondicaoMedica(paciente_id=id, **data.model_dump())
    db.add(pcm)
    db.commit()
    return {"message": "Condição médica associada ao paciente."}

@router.post("/{id}/medicamentos", status_code=status.HTTP_201_CREATED)
def adicionar_medicamento(
    id: int,
    data: MedicamentoCreate,
    db: Session = Depends(get_db),
    aluno: Usuario = Depends(check_perfil([PerfilUsuario.ALUNO]))
):
    med = MedicamentoPaciente(paciente_id=id, **data.model_dump())
    db.add(med)
    db.commit()
    return {"message": "Medicamento registrado com sucesso."}