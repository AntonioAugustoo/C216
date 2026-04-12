import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def assert_default_shape(response, expected_method):
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["method"] == expected_method
    assert "message" in body
    assert isinstance(body["message"], str)
    return body


def test_get_query_tem_fonte_query():
    response = client.get("/api/v1/hello", params={"name": " antonio "})
    body = assert_default_shape(response, "GET")
    assert body["input"]["source"] == "query"
    assert body["input"]["name"] == "Antonio"


def test_get_path_tem_fonte_path():
    response = client.get("/api/v1/hello/antonio")
    body = assert_default_shape(response, "GET")
    assert body["input"]["source"] == "path"
    assert body["message"].endswith("Antonio")


def test_post_retorna_metodo_post():
    response = client.post("/api/v1/hello", json={"name": "Antonio"})
    body = assert_default_shape(response, "POST")
    assert "Cadastro" in body["message"]


def test_put_retorna_metodo_put():
    response = client.put("/api/v1/update", json={"name": "Antonio"})
    body = assert_default_shape(response, "PUT")
    assert "atualizado" in body["message"].lower()


def test_delete_retorna_metodo_delete():
    response = client.delete("/api/v1/delete", params={"name": "Antonio"})
    body = assert_default_shape(response, "DELETE")
    assert "removido" in body["message"].lower()


def test_patch_retorna_metodo_patch():
    response = client.patch("/api/v1/patch", json={"name": "Antonio"})
    body = assert_default_shape(response, "PATCH")
    assert "parcial" in body["message"].lower()


def test_root_retorna_status_basico():
    response = client.get("/")
    body = assert_default_shape(response, "GET")
    assert body["message"] == "API no ar"


@pytest.mark.parametrize("payload", [{}, {"name": ""}])
def test_post_invalido(payload):
    response = client.post("/api/v1/hello", json=payload)
    assert response.status_code in (200, 422)
