# Versão 1.1

from uvicorn import run
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()


class Professor(BaseModel):
    id: int
    nome: str
    email: str


# """Banco"""
Professores = []
# -----------

@app.post("/professor/", response_model=Professor)
def create_professor(professor: Professor):
    if any(p.id == professor.id for p in Professores):
        raise HTTPException(status_code=400, detail="ID já existe")
    if any(p.email == professor.email for p in Professores):
        raise HTTPException(status_code=400, detail="Email já existe")

    Professores.append(professor)
    return professor

@app.get("/professor/", response_model=List[Professor])
def get_professor():
    return Professores

@app.put("/professor/{id}", response_model=Professor)
def update_professor(id: int, updated_prof: Professor):
    for i, prof in enumerate(Professores):
        if prof.id == id:
            Professores[i] = updated_prof
            return updated_prof
    raise HTTPException(status_code=404, detail="Professor não encontrado")

@app.delete("/professor/{id}")
def delete_professor(id: int):
    for i, prof in enumerate(Professores):
        if prof.id == id:
            del Professores[i]
            return {"mensagem": "Professor removido com sucesso"}
    raise HTTPException(status_code=404, detail="Professor não encontrado")

# MENSSAGEM DE TESTE
@app.get("/")
def teste():
    return "A api esta no ar!"
# ------------------

if __name__ == "__main__":
    run(app, port=8000)
