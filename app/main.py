from fastapi import FastAPI
from app.api.routes import auth
from app.db.database import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
