from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
###CONEXION CON LA BASE DE DATOS
 
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:post128bluu@localhost:5432/pgpi"
 
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()