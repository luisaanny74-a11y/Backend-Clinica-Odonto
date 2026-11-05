from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Sistema de Prontuário Odontológico - API"
    API_V1_STR: str = "/api/v1"
    
    # Configurações do MySQL (Ajustar credenciais em .env)
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DB: str = "clinica_odonto"

    # Supports the DATABASE_URL setting documented in the project README.
    DATABASE_URL: str | None = None

    # Opt-in because these shared test credentials must never be seeded in production.
    SEED_TEST_USERS: bool = False

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

    # JWT Config
    SECRET_KEY: str = "SUA_CHAVE_SECRETA_SUPER_SEGURA_AQUI_CHANGE_IN_PROD"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 horas

settings = Settings()
