from fastapi import Request


async def add_custom_header(request: Request, call_next):
    """Middleware para adicionar header customizado."""
    response = await call_next(request)
    response.headers["X-App-Version"] = "1.0"
    return response
