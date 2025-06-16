from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import DBSala
from schemas import salaBase, salas
from database import get_db

router = APIRouter()


@router.post("/sala/", response_model=salas)
def create_salas(sala: salaBase, db: Session = Depends(get_db)): 
    db_sala = db.query(DBSala).filter(DBSala.numero == sala.numero).first()
    db_sala = DBSala(**sala.model_dump())

    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala 


@router.get("/sala/", response_model=list[salas]) # response_model é List[Sala] (plural)
def read_salas(db: Session = Depends(get_db)):
    return db.query(DBSala).all()


@router.get("/sala/{id_sala}", response_model=salas)
def read_sala(id_sala: int, db: Session = Depends(get_db)):
    db_sala = db.query(DBSala).filter(DBSala.idsalas == id_sala).first()
    if db_sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return db_sala


@router.put("/sala/{id_sala}", response_model=salas)
def update_salas(id_sala: int, updated_sala: salaBase, db: Session = Depends(get_db)):
    db_sala = db.query(DBSala).filter(DBSala.idsalas == id_sala).first()
    if db_sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    
    for field, value in updated_sala.model_dump().items():
        setattr(db_sala, field, value)

    db.commit()
    db.refresh(db_sala)
    return db_sala


@router.delete("/sala/{id_sala}")
def delete_salas(id_sala: int, db: Session = Depends(get_db)): # Recebe a sessão via Depends, nomeie a variável 'id_sala' singular
    db_sala = db.query(DBSala).filter(DBSala.idsalas == id_sala).first()
    if db_sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    db.delete(db_sala)
    db.commit()
    return {"mensagem": f"Sala com ID {id_sala} removida com sucesso"}
