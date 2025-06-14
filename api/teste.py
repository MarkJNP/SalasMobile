# Versão 1.5.1

from uvicorn import run
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from openpyxl import Workbook

app = FastAPI()


class professores(BaseModel):
    idProfessor: int
    Nome: str
    Email: str
    cpf: str
    disciplina: str


class salas(BaseModel):
    idSala: int
    Numero: str
    TipoSala: str
    bloco: str
    Capacidade: int

class reservas(BaseModel):
    idReserva: int
    idProfessor: int
    idSala: int

# Temporarios
Professores = []
Salas = []
Reservas = []
# -----------

# CRUD Professores
@app.post("/professor/", response_model=professores)
def create_professores(professor: professores):
    if any(p.idProfessor == professor.idProfessor for p in Professores):
        raise HTTPException(status_code=400, detail="ID já existe")
    
    if any(p.Email == professor.Email for p in Professores):
        raise HTTPException(status_code=400, detail="Email já existe")

    Professores.append(professor)
    return professor


@app.get("/professor/", response_model=List[professores])
def read_professores():
    return Professores


@app.put("/professor/{id}", response_model=professores)
def update_professores(id: int, updated_prof: professores):
    for i, prof in enumerate(Professores):
        if prof.idProfessor == id:
            Professores[i] = updated_prof
            return updated_prof
    raise HTTPException(status_code=404, detail="Professor não encontrado")


@app.delete("/professor/{id}")
def delete_professores(id: int):
    for i, prof in enumerate(Professores):
        if prof.idProfessor == id:
            del Professores[i]
            return {"mensagem": "Professor removido com sucesso"}
    raise HTTPException(status_code=404, detail="Professor não encontrado")


# CRUD Salas
@app.post("/sala/", response_model=Salas)
def create_salas(salas: salas):
    if any(p.idSala == salas.idSala for p in Salas):
        raise HTTPException(status_code=400, detail="ID já existe")
    Salas.append(salas)
    return Salas


@app.get("/sala/", response_model=List[salas])
def read_salas():
    return Salas


@app.put("/sala/{id}", response_model=salas)
def update_salas(id: int, updated_salas: salas):
    for i, sal in enumerate(Salas):
        if sal.idSala == id:
            Salas[i] = updated_salas
            return updated_salas
    raise HTTPException(status_code=404, detail="Sala não encontrado")


@app.delete("/sala/{id}")
def delete_salas(id: int):
    for i, sal in enumerate(Salas):
        if sal.idSala == id:
            del Salas[i]
            return {"mensagem": "Sala removido com sucesso"}
    raise HTTPException(status_code=404, detail="Sala não encontrado")


@app.post("/reserva/", response_model=reservas)
def create_reservas(reserva: reservas):
    if any(p.idReserva == reserva.idReserva for p in Reservas):
        raise HTTPException(status_code=400, detail="ID da reserva já existe")
        
    if any(p.idProfessor == reserva.idProfessor for p in Reservas):
        raise HTTPException(status_code=400, detail="ID do professor já existe")
    
    if any(p.idSala == reserva.idSala for p in Reservas):
        raise HTTPException(status_code=400, detail="ID da sala já existe")

    Reservas.append(reserva)
    return reserva


# MENSSAGEM DE TESTE
@app.get("/")
def teste():
    return "A api esta no ar!"
# ------------------


# Arquivo Excel 
@app.get("/excel/")
def excel():
    arqExc = Workbook()
    planilha = arqExc.active
    planilha.title = "salasAgendadas"

    planilha.append(["Disciplina", "Professor", "Sala", "Bloco"])

    for reserva in Reservas:
        professor = next((p for p in Professores if p.idProfessor == reserva.idProfessor), None)
        sala = next((s for s in Salas if s.idSala == reserva.idSala), None)
        
        if professor and sala:
            planilha.append([professor.disciplina, professor.Nome, sala.Numero, sala.bloco])
        else:
            planilha.append(["Dados não encontrados", "", "", ""])

    caminho_arquivo = "salasAgendadas.xlsx"
    arqExc.save(caminho_arquivo)

    return FileResponse(
        path=caminho_arquivo,
        filename="salasAgendadas.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    run(app, port=8000)