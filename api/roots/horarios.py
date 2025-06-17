from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import DBHorario
from schemas import Horario, HorarioBase
from database import get_db

router = APIRouter()


@router.post("/horario/", response_model=Horario)
def create_horario(horario: HorarioBase, idreserva: int, db: Session = Depends(get_db)):
    db_horario = DBHorario(**horario.model_dump(), idreserva=idreserva)
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.get("/horario/{idreserva}", response_model=Horario)
def get_horario(idreserva: int, db: Session = Depends(get_db)):
    db_horario = db.query(DBHorario).filter(DBHorario.idreserva == idreserva).first()
    if db_horario is None:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    return db_horario


@router.put("/horario/{idreserva}", response_model=Horario)
def update_horario(idreserva: int, updated_horario: HorarioBase, db: Session = Depends(get_db)):
    db_horario = db.query(DBHorario).filter(DBHorario.idreserva == idreserva).first()
    if db_horario is None:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    for field, value in updated_horario.model_dump().items():
        setattr(db_horario, field, value)

    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.delete("/horario/{idreserva}")
def delete_horario(idreserva: int, db: Session = Depends(get_db)):
    db_horario = db.query(DBHorario).filter(DBHorario.idreserva == idreserva).first()
    if db_horario is None:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    db.delete(db_horario)
    db.commit()
    return {"mensagem": f"Horário da reserva {idreserva} deletado com sucesso"}
