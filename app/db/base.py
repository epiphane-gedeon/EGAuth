from app.db.database import SessionLocal

from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
