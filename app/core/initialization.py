from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from domain.enums import PerfilUsuario
from domain.models import Especialidade, Paciente, Prontuario, Usuario


TEST_USERS = (
    ("Aluno de Teste", "aluno@uninassau.edu.br", "aluno123", "TESTE-ALUNO", PerfilUsuario.ALUNO),
    ("Professor de Teste", "professor@uninassau.edu.br", "professor123", "TESTE-PROF", PerfilUsuario.PROFESSOR),
    ("Recepção de Teste", "recepcao@uninassau.edu.br", "recepcao123", "TESTE-REC", PerfilUsuario.RECEPCAO),
    ("Admin de Teste", "admin@uninassau.edu.br", "admin123", "TESTE-ADMIN", PerfilUsuario.ADMIN),
    ("Coordenadora Admin de Teste", "coordenadora.admin@uninassau.edu.br", "admin123", "TESTE-COORD", PerfilUsuario.ADMIN),
)


def seed_test_users(db: Session) -> int:
    """Create or synchronize local test accounts with real password hashes."""
    changed = 0
    for nome, email, senha, matricula, perfil in TEST_USERS:
        existing = db.query(Usuario).filter(Usuario.email == email).first()
        if existing is not None:
            try:
                password_matches = verify_password(senha, existing.senha_hash)
            except Exception:
                password_matches = False
            if not password_matches or not existing.ativo:
                existing.senha_hash = get_password_hash(senha)
                existing.ativo = True
                changed += 1
            continue
        if db.query(Usuario).filter(Usuario.matricula == matricula).first() is not None:
            # Preserve existing accounts if a local installation already uses this ID.
            continue
        db.add(Usuario(
            nome=nome,
            email=email,
            senha_hash=get_password_hash(senha),
            matricula=matricula,
            perfil=perfil,
            ativo=True,
        ))
        changed += 1
    if changed:
        db.commit()
    return changed


def seed_initial_specialty(db: Session) -> bool:
    """Ensure Semiologia exists without assigning its database-generated ID."""
    existing = (
        db.query(Especialidade)
        .filter(Especialidade.nome.ilike("Semiologia"))
        .first()
    )
    if existing is not None:
        return False

    db.add(Especialidade(nome="Semiologia", ativo=True))
    db.commit()
    return True


def ensure_patient_records(db: Session) -> int:
    """Create missing 1:1 patient records without changing existing rows."""
    patients = (
        db.query(Paciente)
        .outerjoin(Prontuario, Paciente.id == Prontuario.paciente_id)
        .filter(Prontuario.id.is_(None))
        .all()
    )
    if not patients:
        return 0

    db.add_all([Prontuario(paciente_id=patient.id) for patient in patients])
    db.commit()
    return len(patients)
