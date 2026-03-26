from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, books

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ルーターの登録
app.include_router(users.router)
app.include_router(books.router) 

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

    