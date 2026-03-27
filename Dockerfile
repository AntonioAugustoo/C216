FROM python:3.12-slim

WORKDIR /app

COPY crud_alunos_Aula_1.py ./

CMD ["python", "crud_alunos_Aula_1.py"]