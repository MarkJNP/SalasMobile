from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base


class DBProfessor(Base):
    __tablename__ = "professores"

    idprofessor = Column("idProfessor", Integer, primary_key=True, index=True)
    nome = Column("Nome", String(100), nullable=False)
    email = Column("Email", String(100), unique=True, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    disciplina = Column(String(30), nullable=False)

    reservas = relationship("DBReserva", back_populates="professor")


class DBSala(Base):
    __tablename__ = "salas"

    idsala = Column("idSala", Integer, primary_key=True, index=True)
    numero = Column("Numero", String(10), unique=True, nullable=False)
    tiposala = Column("TipoSala", String(50), nullable=False)
    bloco = Column(String(50), nullable=False)
    capacidade = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("capacidade > 0", name="check_capacidade_positiva"),
    )

    reservas = relationship("DBReserva", back_populates="sala")


class DBReserva(Base):
    __tablename__ = "reserva"

    idreserva = Column("idReserva", Integer, primary_key=True, index=True)
    idprofessor = Column("idProfessor", Integer, ForeignKey("professores.idProfessor"), nullable=False)
    idsala = Column("idSala", Integer, ForeignKey("salas.idSala"), nullable=False)

    professor = relationship("DBProfessor", back_populates="reservas")
    sala = relationship("DBSala", back_populates="reservas")
    horario = relationship("DBHorario", uselist=False, back_populates="reserva")


class DBHorario(Base):
    __tablename__ = "horario"

    idreserva = Column("idReserva", Integer, ForeignKey("reserva.idReserva"), primary_key=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    data = Column(Date, nullable=False)

    reserva = relationship("DBReserva", back_populates="horario")

    __table_args__ = (
        CheckConstraint("hora_inicio < hora_fim", name="check_hora_inicio_fim"),
    )
