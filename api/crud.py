# Versão 1.2.2

from uvicorn import run
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class professor(BaseModel):
    idprofessor: int
    nome: str
    email: str
    senha: str


class salas(BaseModel):
    idsalas: int
    numero: str
    tiposala: str
    bloco: str
    capacidade: int

# Temporarios
Professores = []
Salas = []
# -----------

# CRUD Professores
@app.post("/professor/", response_model=professor)
def create_professores(professor: professor):
    if any(p.id == professor.idprofessor for p in Professores):
        raise HTTPException(status_code=400, detail="ID já existe")
    if any(p.email == professor.email for p in Professores):
        raise HTTPException(status_code=400, detail="Email já existe")

    Professores.append(professor)
    return professor


@app.get("/professor/", response_model=List[professor])
def read_professores():
    return Professores


@app.put("/professor/{id}", response_model=professor)
def update_professores(id: int, updated_prof: professor):
    for i, prof in enumerate(Professores):
        if prof.idprofessor == id:
            Professores[i] = updated_prof
            return updated_prof
    raise HTTPException(status_code=404, detail="Professor não encontrado")


@app.delete("/professor/{id}")
def delete_professores(id: int):
    for i, prof in enumerate(Professores):
        if prof.idprofessor == id:
            del Professores[i]
            return {"mensagem": "Professor removido com sucesso"}
    raise HTTPException(status_code=404, detail="Professor não encontrado")


# CRUD Salas
@app.post("/sala/", response_model=Salas)
def create_salas(salas: salas):
    if any(p.idsalas == salas.idsalas for p in Salas):
        raise HTTPException(status_code=400, detail="ID já existe")
    Salas.append(salas)
    return Salas


@app.get("/sala/", response_model=List[salas])
def read_salas():
    return Salas


@app.put("/sala/{id}", response_model=salas)
def update_salas(id: int, updated_salas: salas):
    for i, sal in enumerate(Salas):
        if sal.idsalas == id:
            Salas[i] = updated_salas
            return updated_salas
    raise HTTPException(status_code=404, detail="Sala não encontrado")


@app.delete("/sala/{id}")
def delete_salas(id: int):
    for i, sal in enumerate(Salas):
        if sal.idsalas == id:
            del Salas[i]
            return {"mensagem": "Sala removido com sucesso"}
    raise HTTPException(status_code=404, detail="Sala não encontrado")


# MENSSAGEM DE TESTE
@app.get("/")
def teste():
    return "A api esta no ar!"
# ------------------

if __name__ == "__main__":
    run(app, port=8000)
