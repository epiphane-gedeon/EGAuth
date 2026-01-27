from app.db.database import engine
from app.db.base import Base

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
