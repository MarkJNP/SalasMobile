from pydantic import BaseModel

class ProfessorBase(BaseModel):
    nome: str
    email: str
    senha: str

class Professor(ProfessorBase):
    idprofessor: int
    class Config:
        from_attributes = True

class SalaBase(BaseModel):
    numero: str
    tiposala: str
    bloco: str
    capacidade: int

class Sala(SalaBase):
    idsalas: int
    class Config:
        from_attributes = True
