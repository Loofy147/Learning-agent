from fastapi import FastAPI
from . import models, database
from .routers import trading, questions

app = FastAPI()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

app.include_router(trading.router)
app.include_router(questions.router)
