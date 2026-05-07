from fastapi import FastAPI
from app.routes.aluno_routes import router as aluno_router
from app.middlewares.logging import log_requests
from app.middlewares.custom_header import add_custom_header

app = FastAPI(
    title="Gerenciador de Alunos",
    description="API para gerenciamento de alunos com PostgreSQL",
    version="2.0.0"
)

# Registrar middlewares
app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

# Registrar rotas
app.include_router(aluno_router)


@app.get("/")
async def healthcheck():
    return {"ok": True, "message": "API de alunos no ar"}
