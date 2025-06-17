from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import DBProfessor
from schemas import ProfessorBase, Professor
from database import get_db

router = APIRouter()


@router.post("/professor/", response_model=Professor)
def create_professores(professor: ProfessorBase, db: Session = Depends(get_db)):
    db_professor = db.query(DBProfessor).filter(DBProfessor.email == professor.email).first()
    if db_professor:
        raise HTTPException(status_code=400, detail="Email de professor já existe")

    db_professor = DBProfessor(**professor.model_dump()) 
    db.add(db_professor) 
    db.commit()          
    db.refresh(db_professor)
    return db_professor 


@router.get("/professor/", response_model=list[Professor])
def read_professores(db: Session = Depends(get_db)):
    return db.query(DBProfessor).all()


@router.get("/professor/{id_professor}", response_model=Professor)
def read_professor(id_professor: int, db: Session = Depends(get_db)):
    db_professor = db.query(DBProfessor).filter(DBProfessor.idprofessor == id_professor).first()
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return db_professor


@router.put("/professor/{id_professor}", response_model=Professor)
def update_professores(id_professor: int, updated_prof: ProfessorBase, db: Session = Depends(get_db)):
    db_professor = db.query(DBProfessor).filter(DBProfessor.idprofessor == id_professor).first()
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    for field, value in updated_prof.model_dump().items():
        setattr(db_professor, field, value)

    db.commit()
    db.refresh(db_professor)
    return db_professor


@router.delete("/professor/{id_professor}")
def delete_professores(id_professor: int, db: Session = Depends(get_db)):
    db_professor = db.query(DBProfessor).filter(DBProfessor.idprofessor == id_professor).first()
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    db.delete(db_professor)
    db.commit()
    return {"mensagem": f"Professor com ID {id_professor} removido com sucesso"}
