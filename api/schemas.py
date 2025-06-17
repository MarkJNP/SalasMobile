from pydantic import BaseModel
from datetime import time, date


class ProfessorBase(BaseModel):
    nome: str
    email: str
    cpf: str
    disciplina: str


class Professor(ProfessorBase):
    idprofessor: int

    class Config:
        orm_mode = True


class SalaBase(BaseModel):
    numero: str
    tiposala: str
    bloco: str
    capacidade: int


class Sala(SalaBase):
    idsala: int 

    class Config:
        orm_mode = True



class HorarioBase(BaseModel):
    hora_inicio: time
    hora_fim: time
    data: date


class Horario(HorarioBase):
    idreserva: int

    class Config:
        orm_mode = True


class ReservaBase(BaseModel):
    idprofessor: int
    idsala: int


class Reserva(ReservaBase):
    idreserva: int
    professor: Professor
    sala: Sala
    horario: Horario | None = None  # Pode não existir ainda

    class Config:
        orm_mode = True
