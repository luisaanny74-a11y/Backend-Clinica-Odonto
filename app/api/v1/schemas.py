from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, List
from domain.enums import PerfilUsuario, StatusFicha, TipoAlergia, FaceDente, DecisaoAprovacao

# Auth / User Schemas
class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    matricula: Optional[str] = None
    perfil: PerfilUsuario

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    matricula: Optional[str] = None
    perfil: PerfilUsuario

# Paciente Schemas
class PacienteCreate(BaseModel):
    nome_completo: str
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = None
    celular: Optional[str] = None

class PacienteCreateResponse(BaseModel):
    paciente_id: int
    prontuario_id: int
    nome_completo: str

class PacienteResponse(PacienteCreate):
    id: int
    criado_em: datetime
    class Config:
        from_attributes = True

# Clinica Compartilhada Schemas
class CondicaoMedicaCreate(BaseModel):
    condicao_id: int
    observacao: Optional[str] = None

class AlergiaCreate(BaseModel):
    tipo: TipoAlergia
    agente: str
    reacao: Optional[str] = None

class MedicamentoCreate(BaseModel):
    nome: str
    dosagem: Optional[str] = None
    frequencia: Optional[str] = None
    observacao: Optional[str] = None

# Atendimento Schemas
class AtendimentoCreate(BaseModel):
    prontuario_id: int
    especialidade_id: int

class AtendimentoResponse(BaseModel):
    id: int
    prontuario_id: int
    especialidade_id: int
    aluno_id: int
    iniciado_em: datetime
    class Config:
        from_attributes = True

class SinaisVitaisCreate(BaseModel):
    pressao_sistolica: Optional[int] = None
    pressao_diastolica: Optional[int] = None
    pulso: Optional[int] = None
    frequencia_respiratoria: Optional[int] = None
    temperatura: Optional[float] = None
    peso: Optional[float] = None
    altura: Optional[float] = None
    glicemia: Optional[float] = None

# Ficha & Semiologia Schemas
class FichaSemiologiaBase(BaseModel):
    queixa_principal: Optional[str] = None
    historia_doenca_atual: Optional[str] = None
    antecedentes_familiares: Optional[str] = None
    observacoes_gerais: Optional[str] = None
    diagnostico: Optional[str] = None
    plano_tratamento: Optional[str] = None
    necessita_encaminhamento: Optional[bool] = False
    especialidade_encaminhamento_id: Optional[int] = None
    motivo_encaminhamento: Optional[str] = None

class FichaCreateResponse(BaseModel):
    id: int
    atendimento_id: int
    status: StatusFicha
    versao: int

class FichaResponse(BaseModel):
    id: int
    atendimento_id: int
    tipo: str
    status: StatusFicha
    versao: int
    semiologia: Optional[FichaSemiologiaBase] = None
    class Config:
        from_attributes = True

class AprovacaoCreate(BaseModel):
    decisao: DecisaoAprovacao
    observacao: Optional[str] = None

# Odontograma Schemas
class OdontogramaRegistroCreate(BaseModel):
    numero_dente: int
    face: FaceDente
    condicao_id: int
    observacao: Optional[str] = None