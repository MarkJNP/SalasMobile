# Versão 1.2.2

from uvicorn import run
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Annotated 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:senha@localhost:8080/banco"

engine = create_engine(DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


#---Declaração de ORM
class DBProfessor(Base):
    __tablename__ = "professores"

    idprofessor = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    senha = Column(String(255))

class DBSala(Base):
    __tablename__ = "salas"

    idsalas = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), unique=True,index=True)
    tiposala = Column(String(100))
    bloco = Column(String(50))
    capacidade = Column(Integer)


class professorBase(BaseModel):
    nome: str
    email: str
    senha: str

class professor(professorBase):
    idprofessor: int
    class Config:
        orm_mode = True


class salaBase(BaseModel):
    numero: str
    tiposala: str
    bloco: str
    capacidade: int

class salas(salaBase):
    idsalas: int
    class Config:
        orm_mode = True

#---Fim de declaração de ORM

app = FastAPI()

origins = [
    "http://localhost", # Geralmente não é necessário, mas pode incluir
    "http://localhost:3000", # A porta padrão do React Dev Server (CRA/Vite)
    # Adicione outras origens se seu frontend rodar em outra porta/domínio
]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,         
    allow_origins=["*"],
    allow_credentials=True,  
    allow_methods=["*"],           
    allow_headers=["*"],           
)

def get_db():
    db = SessionLocal() # Cria uma nova sessão
    try:
        yield db # Fornece a sessão para o endpoint
    finally:
        db.close() # Fecha a sessão no final da requisição (mesmo que ocorra erro)

# Use Annotated para injeção de dependência com tipagem
DBSession = Annotated[Session, Depends(get_db)]


# Temporarios
Professores = []
Salas = []
# -----------

# CRUD Professores
@app.post("/professor/", response_model=professor)
def create_professores(professor: professorBase, db: DBSession):
    db_professor = db.query(DBProfessor).filter(DBProfessor.email == professor.email).first()
    if db_professor:
        raise HTTPException(status_code=400, detail="Email de professor já existe")

    db_professor = DBProfessor(**professor.model_dump()) 

    db.add(db_professor) 
    db.commit()          
    db.refresh(db_professor)

    return db_professor 


@app.get("/professor/", response_model=List[professor])
def read_professores(db: DBSession):
    Professores = db.query(DBProfessor).all()
    return Professores

@app.get("/professor/{id_professor}", response_model=Professor)
def read_professor(id_professor: int, db: DBSession):
    db_professor = db.query(DBProfessor).filter(DBProfessor.idprofessor == id_professor).first()
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return db_professor


@app.put("/professor/{id_professor}", response_model=professor)
def update_professores(id: int, updated_prof: professorBase, db: DBSession):
    db_professor = db.query(DBProfessor).filter(DBProfessor.idprofessor == id).first()
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    for i, prof in updated_prof.model_dump().items():
        setattr(db_professor, i, prof)

    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.delete("/professor/{id_professor}")
def delete_professores(id_professor: int, db:DBSession):
    db_professor = db.query(DBProfessor).filter(DBProfessor.idprofessor == id_professor).first()
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor nao encontrado")

    db.delete(db_professor)
    db.commit()
    return {"mensagem": "Professor removido com sucesso"}


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
