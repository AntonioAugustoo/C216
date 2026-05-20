from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class Aluno(BaseModel):
    id: int
    nome: str
    email: str
    curso: str
    matricula: int


class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    curso: Literal["GES", "GEC"]


class AlunoPatch(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
