# versao 1.7
from fastapi import FastAPI
from database import Base, engine
from roots import professores, salas

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(professores.router)
app.include_router(salas.router)
