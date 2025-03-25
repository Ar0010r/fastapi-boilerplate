from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Credentials(BaseSettings):
    pg_host: str
    pg_port: str
    pg_user: str
    pg_password: str
    pg_db: str
    engine_args: dict = {
        "echo": True,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    }
    
    prefix: str = "postgresql+asyncpg"
    # prefix: str = "postgresql_asyncpg"

    def get_pg_url(self):
        return f"{self.prefix}://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"

    model_config = SettingsConfigDict(env_file='/code/.env', case_sensitive=False, env_file_encoding='utf-8', extra='ignore' )

db_creds = Credentials()

engine = create_async_engine(db_creds.get_pg_url(), echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session