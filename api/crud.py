# Versão 1.2.5

from uvicorn import run
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Annotated 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "mysql+pymysql://admmobile:Mobi@\9r_+?-u?5&5^Y4=@localhost:8080/ClassControl"

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
        from_attributes = True


class salaBase(BaseModel):
    numero: str
    tiposala: str
    bloco: str
    capacidade: int

class salas(salaBase):
    idsalas: int
    class Config:
        from_attributes = True

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
    allow_credentials=True,      # 
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

@app.get("/professor/{id_professor}", response_model=professor)
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

# --- CRUD Salas (AGORA USANDO BANCO DE DADOS) ---

@app.post("/sala/", response_model=Salas)
def create_salas(sala: salaBase, db: DBSession): 
    # Verifique se o número da sala já existe
    db_sala = db.query(DBSala).filter(DBSala.numero == sala.numero).first()
    if db_sala:
        raise HTTPException(status_code=400, detail="Número de sala já existe")

    db_sala = DBSala(**sala.model_dump()) # Pydantic v2

    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)

    return db_sala # FastAPI serializa para Sala (singular)

@app.get("/sala/", response_model=List[salas]) # response_model é List[Sala] (plural)
def read_salas(db: DBSession):
    salas = db.query(DBSala).all()
    return salas

# Adicionando endpoint para buscar uma sala por ID
@app.get("/sala/{id_sala}", response_model=salas)
def read_sala(id_sala: int, db: DBSession):
    db_sala = db.query(DBSala).filter(DBSala.idsalas == id_sala).first()
    if db_sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return db_sala


@app.put("/sala/{id_sala}", response_model=salas)
def update_salas(id_sala: int, updated_sala: salaBase, db: DBSession): # Use SalaBase para input, nomeie a variável 'updated_sala' singular
    db_sala = db.query(DBSala).filter(DBSala.idsalas == id_sala).first()
    if db_sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    for field, value in updated_sala.model_dump().items(): # Pydantic v2
        setattr(db_sala, field, value)

    db.commit()
    db.refresh(db_sala)

    return db_sala


@app.delete("/sala/{id_sala}")
def delete_salas(id_sala: int, db: DBSession): # Recebe a sessão via Depends, nomeie a variável 'id_sala' singular
    db_sala = db.query(DBSala).filter(DBSala.idsalas == id_sala).first()
    if db_sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    db.delete(db_sala)
    db.commit()

    return {"mensagem": f"Sala com ID {id_sala} removida com sucesso"}


# MENSSAGEM DE TESTE
@app.get("/")
def teste():
    return "A api esta no ar!"
# ------------------

if __name__ == "__main__":
    # Este bloco irá tentar criar as tabelas no banco na primeira execução
    # Se as tabelas já existirem, ele não fará nada.
    # Em produção, use ferramentas de migração (como Alembic) para gerenciar schema.
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas (ou já existentes).")

    print("Iniciando servidor Uvicorn...")
    run(app, host="0.0.0.0", port=8000) # Use 0.0.0.0 para ser acessível externamente se necessário
