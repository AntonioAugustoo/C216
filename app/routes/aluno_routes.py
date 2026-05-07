from fastapi import APIRouter, HTTPException
from app.schemas.aluno import Aluno, AlunoCreate, AlunoPatch
from app.services.aluno_service import AlunoService

router = APIRouter(prefix="/api/v1", tags=["alunos"])
service = AlunoService()


@router.get("/alunos/", response_model=dict)
async def listar_alunos():
    """Lista todos os alunos."""
    alunos = await service.listar()
    return {"total": len(alunos), "alunos": alunos}


@router.get("/alunos/{aluno_id}", response_model=Aluno)
async def buscar_aluno(aluno_id: int):
    """Busca um aluno por ID."""
    aluno = await service.buscar_por_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="aluno nao encontrado")
    return aluno


@router.post("/alunos/", status_code=201, response_model=Aluno)
async def criar_aluno(aluno: AlunoCreate):
    """Cria um novo aluno."""
    try:
        return await service.criar(aluno)
    except Exception as e:
        if "email" in str(e).lower():
            raise HTTPException(status_code=400, detail="email ja cadastrado")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/alunos/{aluno_id}", response_model=Aluno)
async def atualizar_aluno(aluno_id: int, aluno: AlunoPatch):
    """Atualiza um aluno existente."""
    # Se apenas nome or email for fornecido, buscar o aluno atual e manter os outros campos
    aluno_atual = await service.buscar_por_id(aluno_id)
    if not aluno_atual:
        raise HTTPException(status_code=404, detail="aluno nao encontrado")
    
    update_data = aluno.model_dump(exclude_unset=True)
    nome = update_data.get("nome", aluno_atual["nome"])
    email = update_data.get("email", aluno_atual["email"])
    
    aluno_completo = AlunoCreate(
        nome=nome,
        email=email,
        curso=aluno_atual["curso"]
    )
    
    try:
        atualizado = await service.atualizar(aluno_id, aluno_completo)
        if not atualizado:
            raise HTTPException(status_code=404, detail="aluno nao encontrado")
        return atualizado
    except Exception as e:
        if "email" in str(e).lower():
            raise HTTPException(status_code=400, detail="email ja cadastrado")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/alunos/{aluno_id}")
async def deletar_aluno(aluno_id: int):
    """Deleta um aluno."""
    aluno = await service.buscar_por_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="aluno nao encontrado")
    
    sucesso = await service.deletar(aluno_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="aluno nao encontrado")
    return {"deleted": True, "aluno": aluno}


@router.delete("/alunos/")
async def resetar_alunos():
    """Deleta todos os alunos."""
    deleted_count = await service.resetar()
    return {"deleted": True, "total_removidos": deleted_count}
