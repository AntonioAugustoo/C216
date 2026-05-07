import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://alunos_user:alunos_password@db:5432/alunos_db"
)


async def get_connection():
    """Obtém uma conexão com o banco de dados PostgreSQL."""
    return await asyncpg.connect(DATABASE_URL)
