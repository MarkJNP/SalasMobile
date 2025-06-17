from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import DBReserva
from schemas import Reserva, ReservaBase
from database import get_db

router = APIRouter()


@router.post("/reserva/", response_model=Reserva)
def create_reserva(reserva: ReservaBase, db: Session = Depends(get_db)):
    db_reserva = DBReserva(**reserva.model_dump())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


@router.get("/reserva/", response_model=list[Reserva])
def read_reservas(db: Session = Depends(get_db)):
    return db.query(DBReserva).all()


@router.get("/reserva/{id_reserva}", response_model=Reserva)
def read_reserva(id_reserva: int, db: Session = Depends(get_db)):
    db_reserva = db.query(DBReserva).filter(DBReserva.idreserva == id_reserva).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    return db_reserva


@router.put("/reserva/{id_reserva}", response_model=Reserva)
def update_reserva(id_reserva: int, updated_reserva: ReservaBase, db: Session = Depends(get_db)):
    db_reserva = db.query(DBReserva).filter(DBReserva.idreserva == id_reserva).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    for field, value in updated_reserva.model_dump().items():
        setattr(db_reserva, field, value)

    db.commit()
    db.refresh(db_reserva)
    return db_reserva


@router.delete("/reserva/{id_reserva}")
def delete_reserva(id_reserva: int, db: Session = Depends(get_db)):
    db_reserva = db.query(DBReserva).filter(DBReserva.idreserva == id_reserva).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    db.delete(db_reserva)
    db.commit()
    return {"mensagem": f"Reserva {id_reserva} deletada com sucesso"}
