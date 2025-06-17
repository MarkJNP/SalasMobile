from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, CheckConstraint
from sqlalchemy.orm import relationship
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
    numero = Column(String(50), unique=True, index=True)
    tiposala = Column(String(100))
    bloco = Column(String(50))
    capacidade = Column(Integer)


class DBReserva(Base):
    __tablename__ = "reserva"

    idreserva = Column(Integer, primary_key=True, index=True)
    idprofessor = Column(Integer, ForeignKey("professores.idprofessor"))
    idsala = Column(Integer, ForeignKey("salas.idsalas"))

    professor = relationship("DBProfessor")
    sala = relationship("DBSala")
    horario = relationship("DBHorario", uselist=False, back_populates="reserva")


class DBHorario(Base):
    __tablename__ = "horario"

    idreserva = Column(Integer, ForeignKey("reserva.idreserva"), primary_key=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    data = Column(Date, nullable=False)

    reserva = relationship("DBReserva", back_populates="horario")

    __table_args__ = (
        CheckConstraint("hora_inicio < hora_fim", name="check_hora_inicio_fim"),
    )
