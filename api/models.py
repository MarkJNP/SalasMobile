from sqlalchemy import Column, Integer, String
from database import Base

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
    