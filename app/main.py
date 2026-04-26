from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

app = FastAPI(title="Gerenciador de Alunos")

VALID_COURSES = {"GES", "GEC"}


class AlunoCreate(BaseModel):
    nome: str = Field(min_length=1)
    email: EmailStr
    curso: str

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("nome nao pode ser vazio")
        return cleaned

    @field_validator("curso")
    @classmethod
    def validate_curso(cls, value: str) -> str:
        normalized = value.strip().upper()
        if normalized not in VALID_COURSES:
            raise ValueError("curso deve ser GES ou GEC")
        return normalized


class AlunoPatch(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("nome nao pode ser vazio")
        return cleaned


alunos: dict[str, dict] = {}
curso_counters = {"GES": 0, "GEC": 0}


def serialize_alunos() -> list[dict]:
    return [alunos[key] for key in sorted(alunos.keys())]


@app.get("/")
async def healthcheck():
    return {"ok": True, "message": "API de alunos no ar"}


@app.post("/api/v1/alunos/", status_code=201)
async def create_aluno(payload: AlunoCreate):
    curso_counters[payload.curso] += 1
    matricula = curso_counters[payload.curso]
    aluno_id = f"{payload.curso}{matricula}"

    aluno = {
        "id": aluno_id,
        "nome": payload.nome,
        "email": payload.email,
        "curso": payload.curso,
        "matricula": matricula,
    }
    alunos[aluno_id] = aluno
    return aluno


@app.get("/api/v1/alunos/")
async def list_alunos():
    return {"total": len(alunos), "alunos": serialize_alunos()}


@app.get("/api/v1/alunos/{aluno_id}")
async def get_aluno(aluno_id: str):
    aluno = alunos.get(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="aluno nao encontrado")
    return aluno


@app.patch("/api/v1/alunos/{aluno_id}")
async def patch_aluno(aluno_id: str, payload: AlunoPatch):
    aluno = alunos.get(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="aluno nao encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    aluno.update(update_data)
    return aluno


@app.delete("/api/v1/alunos/{aluno_id}")
async def delete_aluno(aluno_id: str):
    if aluno_id not in alunos:
        raise HTTPException(status_code=404, detail="aluno nao encontrado")
    deleted = alunos.pop(aluno_id)
    return {"deleted": True, "aluno": deleted}


@app.delete("/api/v1/alunos/")
async def reset_alunos():
    deleted_count = len(alunos)
    alunos.clear()
    return {"deleted": True, "total_removidos": deleted_count}
