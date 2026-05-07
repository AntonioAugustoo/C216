# 🚀 C216 — Gerenciador de Alunos

Bem-vindo(a)! Este repositório é um repositorio educacional da materia de sistemas distribuidos para gerenciar informações de alunos, pensado como base para exercícios e práticas acadêmicas. O objetivo é servir como um exemplo simples de API com camadas mínimas e persistência.

✨ Visão geral

- Projeto didático para implementar e experimentar conceitos de APIs REST.
- Código organizado de forma clara para facilitar estudos e adaptações.
- Foco em legibilidade, testes básicos e deploy em ambiente containerizado.

🧩 O que você encontra aqui

- Estrutura de uma API web (endpoints, modelos de dados e serviços).
- Camadas separadas para facilitar manutenção e entendimento.
- Testes automatizados básicos para validar o comportamento.
- Arquivos de configuração para executar em containers (Docker).

⚙️ Tecnologias (exemplos)

- Python, FastAPI
- Pydantic para modelos/schemas
- Banco relacional (ex.: PostgreSQL)
- Testes com pytest

🏃⚙️ Como rodar o projeto

**Pré-requisitos:**
- Docker e Docker Compose instalados (recomendado)
- Ou: Python 3.10+ e PostgreSQL (execução local)

**Com Docker Compose (mais fácil):**

```bash
docker compose up --build
```


**Localmente (sem Docker):**

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar as tabelas no banco (certifique-se que PostgreSQL está rodando)
psql -U alunos_user -d alunos_db -f app/db/init.sql

# Iniciar a API
uvicorn app.main:app --reload

# Em outro terminal, rodar os testes
pytest tests/ -v
```

💡 Boas práticas demonstradas

- Separação de responsabilidades entre camadas
- Validações de entrada usando modelos
- Testes automatizados para fluxos essenciais
- Uso de containers para facilitar execução e isolamento

🤝 Como contribuir

- Faça um fork, crie uma branch com sua feature ou correção, e abra um pull request.
- Mantenha as mudanças pequenas e focadas, com testes quando aplicável.

📝 Observações

- Este repositório tem fins pedagógicos; sinta-se à vontade para adaptar e simplificar conforme suas necessidades.





Feito com ❤️ por Antonio Augusto.

