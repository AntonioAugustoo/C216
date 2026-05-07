DROP TABLE IF EXISTS alunos;

CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    curso TEXT NOT NULL CHECK (curso IN ('GES', 'GEC')),
    matricula INTEGER NOT NULL
);

CREATE INDEX idx_alunos_email ON alunos(email);
CREATE INDEX idx_alunos_curso ON alunos(curso);
