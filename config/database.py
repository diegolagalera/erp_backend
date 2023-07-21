from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# CONNEXION A BASE DE DATOS
SQLALCHEMY_DATABSE_URL = os.getenv("DATA_BASE_URL")
engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal= sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def user_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()