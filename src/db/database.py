from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./tetrick.db"

dbEngine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False})
sessaoLocal = sessionmaker(autocommit=False,autoflush=False,bind=dbEngine)

class Base(DeclarativeBase):
    pass 

def getDatabase():
    db = sessaoLocal()
    try:
        yield db
    finally:
        db.close()