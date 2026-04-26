from fastapi.testclient import TestClient

from app.main import app, alunos, curso_counters


client = TestClient(app)


def reset_state():
    alunos.clear()
    curso_counters["GES"] = 0
    curso_counters["GEC"] = 0


def create_many(course: str, amount: int) -> list[str]:
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
        assert response.status_code == 201
        ids.append(response.json()["id"])
    return ids


def test_crud_completo_alunos():
    reset_state()

    ges_ids = create_many("GES", 3)
    gec_ids = create_many("GEC", 3)

    assert ges_ids == ["GES1", "GES2", "GES3"]
    assert gec_ids == ["GEC1", "GEC2", "GEC3"]

    list_response = client.get("/api/v1/alunos/")
    assert list_response.status_code == 200
    listed = list_response.json()
    assert listed["total"] == 6
    assert len(listed["alunos"]) == 6

    get_response = client.get("/api/v1/alunos/GES2")
    assert get_response.status_code == 200
    aluno = get_response.json()
    assert aluno["id"] == "GES2"
    assert aluno["curso"] == "GES"
    assert aluno["matricula"] == 2

    patch_response = client.patch(
        "/api/v1/alunos/GES2",
        json={"nome": "Aluno GES 2 Atualizado", "email": "ges2novo@mail.com"},
    )
    assert patch_response.status_code == 200
    patched = patch_response.json()
    assert patched["nome"] == "Aluno GES 2 Atualizado"
    assert patched["email"] == "ges2novo@mail.com"

    delete_one = client.delete("/api/v1/alunos/GES2")
    assert delete_one.status_code == 200
    assert delete_one.json()["deleted"] is True

    new_ges = client.post(
        "/api/v1/alunos/",
        json={"nome": "Aluno GES Novo", "email": "gesnovo@mail.com", "curso": "GES"},
    )
    assert new_ges.status_code == 201
    assert new_ges.json()["id"] == "GES4"

    reset_response = client.delete("/api/v1/alunos/")
    assert reset_response.status_code == 200
    assert reset_response.json()["deleted"] is True

    list_after_reset = client.get("/api/v1/alunos/")
    assert list_after_reset.status_code == 200
    assert list_after_reset.json()["total"] == 0

    after_reset_create = client.post(
        "/api/v1/alunos/",
        json={"nome": "Aluno GEC Pos Reset", "email": "gec4@mail.com", "curso": "GEC"},
    )
    assert after_reset_create.status_code == 201
    assert after_reset_create.json()["id"] == "GEC4"


def test_busca_de_aluno_inexistente_retorna_404():
    reset_state()
    response = client.get("/api/v1/alunos/GES999")
    assert response.status_code == 404


def test_curso_invalido_retorna_422():
    reset_state()
    response = client.post(
        "/api/v1/alunos/",
        json={"nome": "Aluno X", "email": "x@mail.com", "curso": "ADM"},
    )
    assert response.status_code == 422
