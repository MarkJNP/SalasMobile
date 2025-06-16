from pydantic import BaseModel


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
        