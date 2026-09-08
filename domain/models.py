from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date, Text,
    Enum, ForeignKey, Numeric
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from domain.enums import PerfilUsuario, StatusFicha, TipoAlergia, FaceDente, DecisaoAprovacao

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)
    matricula = Column(String(30), unique=True, nullable=True)
    perfil = Column(Enum(PerfilUsuario), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_completo = Column(String(150), nullable=False)
    cpf = Column(String(11), unique=True, nullable=True, index=True)
    rg = Column(String(30), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String(30), nullable=True)
    estado_civil = Column(String(30), nullable=True)
    etnia = Column(String(50), nullable=True)
    naturalidade = Column(String(100), nullable=True)
    endereco = Column(String(255), nullable=True)
    cep = Column(String(8), nullable=True)
    uf = Column(String(2), nullable=True)
    telefone = Column(String(20), nullable=True)
    celular = Column(String(20), nullable=True)
    profissao = Column(String(100), nullable=True)
    escolaridade = Column(String(100), nullable=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    prontuario = relationship("Prontuario", back_populates="paciente", uselist=False)
    alergias = relationship("Alergia", back_populates="paciente")
    medicamentos = relationship("MedicamentoPaciente", back_populates="paciente")
    condicoes_medicas = relationship("PacienteCondicaoMedica", back_populates="paciente")

class Prontuario(Base):
    __tablename__ = "prontuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False, unique=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="prontuario")
    atendimentos = relationship("Atendimento", back_populates="prontuario")
    odontogramas = relationship("Odontograma", back_populates="prontuario")

class Especialidade(Base):
    __tablename__ = "especialidades"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    ativo = Column(Boolean, nullable=False, default=True)

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prontuario_id = Column(Integer, ForeignKey("prontuarios.id"), nullable=False)
    especialidade_id = Column(Integer, ForeignKey("especialidades.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    iniciado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    finalizado_em = Column(DateTime, nullable=True)

    prontuario = relationship("Prontuario", back_populates="atendimentos")
    aluno = relationship("Usuario")
    especialidade = relationship("Especialidade")
    fichas = relationship("Ficha", back_populates="atendimento")
    sinais_vitais = relationship("SinaisVitais", back_populates="atendimento")

class Ficha(Base):
    __tablename__ = "fichas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    status = Column(Enum(StatusFicha), nullable=False, default=StatusFicha.RASCUNHO)
    versao = Column(Integer, nullable=False, default=1)
    criada_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    enviada_em = Column(DateTime, nullable=True)
    aprovada_em = Column(DateTime, nullable=True)

    atendimento = relationship("Atendimento", back_populates="fichas")
    semiologia = relationship("FichaSemiologia", back_populates="ficha", uselist=False)
    aprovacoes = relationship("Aprovacao", back_populates="ficha")
    historico_status = relationship("HistoricoStatusFicha", back_populates="ficha")

class FichaSemiologia(Base):
    __tablename__ = "fichas_semiologia"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey("fichas.id"), nullable=False, unique=True)
    queixa_principal = Column(Text, nullable=True)
    historia_doenca_atual = Column(Text, nullable=True)
    antecedentes_familiares = Column(Text, nullable=True)
    observacoes_gerais = Column(Text, nullable=True)
    diagnostico = Column(Text, nullable=True)
    plano_tratamento = Column(Text, nullable=True)
    necessita_encaminhamento = Column(Boolean, default=False)
    especialidade_encaminhamento_id = Column(Integer, ForeignKey("especialidades.id"), nullable=True)
    motivo_encaminhamento = Column(Text, nullable=True)

    ficha = relationship("Ficha", back_populates="semiologia")

class CondicaoMedica(Base):
    __tablename__ = "condicoes_medicas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)

class PacienteCondicaoMedica(Base):
    __tablename__ = "paciente_condicoes_medicas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    condicao_id = Column(Integer, ForeignKey("condicoes_medicas.id"), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    observacao = Column(Text, nullable=True)
    registrado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="condicoes_medicas")
    condicao = relationship("CondicaoMedica")

class Alergia(Base):
    __tablename__ = "alergias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo = Column(Enum(TipoAlergia), nullable=False)
    agente = Column(String(150), nullable=False)
    reacao = Column(Text, nullable=True)
    ativa = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="alergias")

class MedicamentoPaciente(Base):
    __tablename__ = "medicamentos_paciente"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    nome = Column(String(150), nullable=False)
    dosagem = Column(String(100), nullable=True)
    frequencia = Column(String(100), nullable=True)
    observacao = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="medicamentos")

class SinaisVitais(Base):
    __tablename__ = "sinais_vitais"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False)
    pressao_sistolica = Column(Integer, nullable=True)
    pressao_diastolica = Column(Integer, nullable=True)
    pulso = Column(Integer, nullable=True)
    frequencia_respiratoria = Column(Integer, nullable=True)
    temperatura = Column(Numeric(4, 1), nullable=True)
    peso = Column(Numeric(5, 2), nullable=True)
    altura = Column(Numeric(4, 2), nullable=True)
    glicemia = Column(Numeric(6, 2), nullable=True)
    registrado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    registrado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    atendimento = relationship("Atendimento", back_populates="sinais_vitais")

class Odontograma(Base):
    __tablename__ = "odontogramas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prontuario_id = Column(Integer, ForeignKey("prontuarios.id"), nullable=False)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    prontuario = relationship("Prontuario", back_populates="odontogramas")
    registros = relationship("OdontogramaRegistro", back_populates="odontograma")

class CondicaoOdontologica(Base):
    __tablename__ = "condicoes_odontologicas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(50), nullable=False, unique=True)
    nome = Column(String(150), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)

class OdontogramaRegistro(Base):
    __tablename__ = "odontograma_registros"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    odontograma_id = Column(Integer, ForeignKey("odontogramas.id"), nullable=False)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False)
    numero_dente = Column(Integer, nullable=False)
    face = Column(Enum(FaceDente), nullable=False)
    condicao_id = Column(Integer, ForeignKey("condicoes_odontologicas.id"), nullable=False)
    observacao = Column(Text, nullable=True)
    registrado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    registrado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    odontograma = relationship("Odontograma", back_populates="registros")

class Aprovacao(Base):
    __tablename__ = "aprovacoes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey("fichas.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    decisao = Column(Enum(DecisaoAprovacao), nullable=False)
    observacao = Column(Text, nullable=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    ficha = relationship("Ficha", back_populates="aprovacoes")

class HistoricoStatusFicha(Base):
    __tablename__ = "historico_status_ficha"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ficha_id = Column(Integer, ForeignKey("fichas.id"), nullable=False)
    status_anterior = Column(String(50), nullable=True)
    status_novo = Column(String(50), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)

    ficha = relationship("Ficha", back_populates="historico_status")