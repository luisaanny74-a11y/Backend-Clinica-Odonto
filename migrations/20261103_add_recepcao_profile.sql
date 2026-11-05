-- Add the receptionist role while preserving existing user profile values.
-- Apply this once to databases whose usuarios.perfil column was created from
-- the previous PerfilUsuario enum.
ALTER TABLE usuarios
    MODIFY COLUMN perfil ENUM('ALUNO', 'PROFESSOR', 'ADMIN', 'RECEPCAO') NOT NULL;
