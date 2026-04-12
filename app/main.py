from fastapi import FastAPI, Request
from pydantic import BaseModel
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url.path} - {process_time:.4f}s")
    return response


class User(BaseModel):
    name: str


def normalize_name(value: str) -> str:
    return value.strip().title()


# GET
@app.get("/")
async def hello_world():
    return {"ok": True, "method": "GET", "message": "API no ar"}


@app.get("/api/v1/hello")
async def hello_name_via_query(name: str):
    clean_name = normalize_name(name)
    return {
        "ok": True,
        "method": "GET",
        "input": {"name": clean_name, "source": "query"},
        "message": f"Ola, {clean_name}",
    }


@app.get("/api/v1/hello/{name}")
async def hello_name_via_path(name: str):
    clean_name = normalize_name(name)
    return {
        "ok": True,
        "method": "GET",
        "input": {"name": clean_name, "source": "path"},
        "message": f"Ola, {clean_name}",
    }


# POST
@app.post("/api/v1/hello")
async def hello_name(user: User):
    clean_name = normalize_name(user.name)
    return {
        "ok": True,
        "method": "POST",
        "input": {"name": clean_name},
        "message": f"Cadastro recebido para {clean_name}",
    }


# PUT
@app.put("/api/v1/update")
async def user_update(user: User):
    clean_name = normalize_name(user.name)
    return {
        "ok": True,
        "method": "PUT",
        "input": {"name": clean_name},
        "message": f"Registro atualizado para {clean_name}",
    }


# DELETE
@app.delete("/api/v1/delete")
async def delete_user_by_name(name: str):
    clean_name = normalize_name(name)
    return {
        "ok": True,
        "method": "DELETE",
        "input": {"name": clean_name},
        "message": f"Registro removido: {clean_name}",
    }


# PATCH
@app.patch("/api/v1/patch")
async def patch_user(user: User):
    clean_name = normalize_name(user.name)
    return {
        "ok": True,
        "method": "PATCH",
        "input": {"name": clean_name},
        "message": f"Atualizacao parcial aplicada em {clean_name}",
    }
