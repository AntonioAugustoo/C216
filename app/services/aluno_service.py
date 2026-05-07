from app.db.connection import get_connection
from app.schemas.aluno import Aluno, AlunoCreate


class AlunoService:
    """Service para operações com Alunos no PostgreSQL."""

    async def listar(self) -> list[dict]:
        """Lista todos os alunos ordenados por ID."""
        conn = await get_connection()
        try:
            rows = await conn.fetch("SELECT id, nome, email, curso, matricula FROM alunos ORDER BY id")
            return [dict(row) for row in rows]
        finally:
            await conn.close()

    async def buscar_por_id(self, aluno_id: int) -> dict | None:
        """Busca um aluno por ID."""
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT id, nome, email, curso, matricula FROM alunos WHERE id=$1",
                aluno_id
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def criar(self, aluno: AlunoCreate) -> dict:
        """Cria um novo aluno."""
        conn = await get_connection()
        try:
            # Obter próximo número de matrícula para o curso (usando MAX, não COUNT)
            result = await conn.fetchval(
                "SELECT COALESCE(MAX(matricula), 0) FROM alunos WHERE curso=$1",
                aluno.curso
            )
            matricula = result + 1

            row = await conn.fetchrow(
                """
                INSERT INTO alunos (nome, email, curso, matricula)
                VALUES ($1, $2, $3, $4)
                RETURNING id, nome, email, curso, matricula
                """,
                aluno.nome, aluno.email, aluno.curso, matricula
            )
            return dict(row)
        finally:
            await conn.close()

    async def atualizar(self, aluno_id: int, aluno: AlunoCreate) -> dict | None:
        """Atualiza um aluno existente."""
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                """
                UPDATE alunos
                SET nome=$1, email=$2, curso=$3
                WHERE id=$4
                RETURNING id, nome, email, curso, matricula
                """,
                aluno.nome, aluno.email, aluno.curso, aluno_id
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def deletar(self, aluno_id: int) -> bool:
        """Deleta um aluno."""
        conn = await get_connection()
        try:
            result = await conn.execute(
                "DELETE FROM alunos WHERE id=$1",
                aluno_id
            )
            return result == "DELETE 1"
        finally:
            await conn.close()

    async def resetar(self) -> int:
        """Deleta todos os alunos e retorna a quantidade deletada."""
        conn = await get_connection()
        try:
            deleted_count = await conn.fetchval("SELECT COUNT(*) FROM alunos")
            await conn.execute("DELETE FROM alunos")
            # Resetar sequência de ID
            await conn.execute("ALTER SEQUENCE alunos_id_seq RESTART WITH 1")
            return deleted_count
        finally:
            await conn.close()
