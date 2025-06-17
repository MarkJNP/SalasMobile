from fastapi import FastAPI
from database import Base, engine
from roots import professores, salas, reservas, horarios

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(professores.router)
app.include_router(salas.router)
app.include_router(reservas.router)
app.include_router(horarios.router)
