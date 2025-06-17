from pydantic import BaseModel
from datetime import time, date


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


class ReservaBase(BaseModel):
    idprofessor: int
    idsala: int

class Reserva(ReservaBase):
    idreserva: int
    class Config:
        from_attributes = True


class HorarioBase(BaseModel):
    hora_inicio: time
    hora_fim: time
    data: date

class Horario(HorarioBase):
    idreserva: int
    class Config:
        from_attributes = True
