import asyncio
import asyncpg
from fastapi.testclient import TestClient
import os

from app.main import app

client = TestClient(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://alunos_user:alunos_password@db:5432/alunos_db"
)


async def reset_database():
    """Limpa todos os dados do banco de dados e reseta a sequência."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute("DELETE FROM alunos")
        await conn.execute("ALTER SEQUENCE alunos_id_seq RESTART WITH 1")
    finally:
        await conn.close()


def reset_state():
    """Reseta o estado do banco para cada teste."""
    asyncio.run(reset_database())


def create_many(course: str, amount: int) -> list[int]:
    """Cria múltiplos alunos e retorna suas IDs."""
    ids = []
    for index in range(1, amount + 1):
        response = client.post(
            "/api/v1/alunos/",
            json={
                "nome": f"Aluno {course} {index}",
                "email": f"{course.lower()}{index}@mail.com",
                "curso": course,
            },
        )
        assert response.status_code == 201, f"Erro ao criar aluno: {response.text}"
        ids.append(response.json()["id"])
    return ids


def test_crud_completo_alunos():
    """Testa CRUD completo de alunos."""
    reset_state()

    # Criar 3 alunos em GES
    ges_ids = create_many("GES", 3)
    # Criar 3 alunos em GEC
    gec_ids = create_many("GEC", 3)

    assert len(ges_ids) == 3
    assert len(gec_ids) == 3

    # Listar todos os alunos
    list_response = client.get("/api/v1/alunos/")
    assert list_response.status_code == 200
    listed = list_response.json()
    assert listed["total"] == 6
    assert len(listed["alunos"]) == 6

    # Buscar aluno específico
    get_response = client.get(f"/api/v1/alunos/{ges_ids[1]}")
    assert get_response.status_code == 200
    aluno = get_response.json()
    assert aluno["id"] == ges_ids[1]
    assert aluno["curso"] == "GES"
    assert aluno["matricula"] == 2

    # Atualizar aluno
    patch_response = client.patch(
        f"/api/v1/alunos/{ges_ids[1]}",
        json={"nome": "Aluno GES 2 Atualizado", "email": "ges2novo@mail.com"},
    )
    assert patch_response.status_code == 200
    patched = patch_response.json()
    assert patched["nome"] == "Aluno GES 2 Atualizado"
    assert patched["email"] == "ges2novo@mail.com"

    # Deletar aluno
    delete_one = client.delete(f"/api/v1/alunos/{ges_ids[1]}")
    assert delete_one.status_code == 200
    assert delete_one.json()["deleted"] is True

    # Criar novo aluno após deletar
    new_ges = client.post(
        "/api/v1/alunos/",
        json={"nome": "Aluno GES Novo", "email": "gesnovo@mail.com", "curso": "GES"},
    )
    assert new_ges.status_code == 201
    assert new_ges.json()["matricula"] == 4

    # Resetar todos os alunos
    reset_response = client.delete("/api/v1/alunos/")
    assert reset_response.status_code == 200
    assert reset_response.json()["deleted"] is True

    # Verificar que foram deletados
    list_after_reset = client.get("/api/v1/alunos/")
    assert list_after_reset.status_code == 200
    assert list_after_reset.json()["total"] == 0

    # Criar aluno após reset
    after_reset_create = client.post(
        "/api/v1/alunos/",
        json={"nome": "Aluno GEC Pos Reset", "email": "gec4@mail.com", "curso": "GEC"},
    )
    assert after_reset_create.status_code == 201


def test_busca_de_aluno_inexistente_retorna_404():
    """Testa busca de aluno que não existe."""
    reset_state()
    response = client.get("/api/v1/alunos/9999")
    assert response.status_code == 404


def test_curso_invalido_retorna_422():
    """Testa criação com curso inválido."""
    reset_state()
    response = client.post(
        "/api/v1/alunos/",
        json={"nome": "Aluno X", "email": "x@mail.com", "curso": "ADM"},
    )
    assert response.status_code == 422


def test_criacao_e_persistencia_de_dados():
    """Testa se os dados são persistidos no banco de dados."""
    reset_state()
    
    # Criar 3 alunos em GES
    ids = create_many("GES", 3)

    # Listar alunos e verificar persistência
    list_response = client.get("/api/v1/alunos/")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 3
    
    # Buscar aluno específico e verificar dados
    get_response = client.get(f"/api/v1/alunos/{ids[0]}")
    assert get_response.status_code == 200
    aluno = get_response.json()
    assert aluno["nome"] == "Aluno GES 1"
    assert aluno["email"] == "ges1@mail.com"


def test_email_unico():
    """Testa se emails duplicados não são permitidos."""
    reset_state()
    
    # Criar primeiro aluno
    response1 = client.post(
        "/api/v1/alunos/",
        json={
            "nome": "Aluno 1",
            "email": "teste@mail.com",
            "curso": "GES",
        },
    )
    assert response1.status_code == 201
    
    # Tentar criar com mesmo email
    response2 = client.post(
        "/api/v1/alunos/",
        json={
            "nome": "Aluno 2",
            "email": "teste@mail.com",
            "curso": "GEC",
        },
    )
    assert response2.status_code == 400


def test_atualizacao_dados():
    """Testa atualização de dados de alunos."""
    reset_state()
    
    # Criar aluno
    create_response = client.post(
        "/api/v1/alunos/",
        json={
            "nome": "Nome Original",
            "email": "original@mail.com",
            "curso": "GES",
        },
    )
    assert create_response.status_code == 201
    aluno_id = create_response.json()["id"]
    
    # Atualizar dados
    patch_response = client.patch(
        f"/api/v1/alunos/{aluno_id}",
        json={"nome": "Nome Atualizado", "email": "atualizado@mail.com"},
    )
    assert patch_response.status_code == 200
    updated = patch_response.json()
    assert updated["nome"] == "Nome Atualizado"
    assert updated["email"] == "atualizado@mail.com"
    
    # Verificar persistência da atualização
    get_response = client.get(f"/api/v1/alunos/{aluno_id}")
    assert get_response.status_code == 200
    assert get_response.json()["nome"] == "Nome Atualizado"


def test_remocao_alunos():
    """Testa remoção de alunos do banco de dados."""
    reset_state()
    
    # Criar 3 alunos
    ids = create_many("GES", 3)
    
    # Verificar total antes da remoção
    list_response = client.get("/api/v1/alunos/")
    assert list_response.json()["total"] == 3
    
    # Remover um aluno
    delete_response = client.delete(f"/api/v1/alunos/{ids[0]}")
    assert delete_response.status_code == 200
    assert delete_response.json()["deleted"] is True
    
    # Verificar que foi removido
    list_response = client.get("/api/v1/alunos/")
    assert list_response.json()["total"] == 2
    
    # Tentar buscar aluno removido
    get_response = client.get(f"/api/v1/alunos/{ids[0]}")
    assert get_response.status_code == 404


def test_adicao_multiplos_alunos_por_curso():
    """Testa adição de múltiplos alunos por curso e validação de matrícula."""
    reset_state()
    
    # Criar 3 alunos em GES
    ges_ids = create_many("GES", 3)
    
    # Criar 3 alunos em GEC
    gec_ids = create_many("GEC", 3)
    
    # Verificar que as matrículas são corretas
    for i, aluno_id in enumerate(ges_ids, 1):
        response = client.get(f"/api/v1/alunos/{aluno_id}")
        assert response.json()["matricula"] == i
        assert response.json()["curso"] == "GES"
    
    for i, aluno_id in enumerate(gec_ids, 1):
        response = client.get(f"/api/v1/alunos/{aluno_id}")
        assert response.json()["matricula"] == i
        assert response.json()["curso"] == "GEC"
