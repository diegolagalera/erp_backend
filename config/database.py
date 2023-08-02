from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import pytest
# CONNEXION A BASE DE DATOS
ENV = os.getenv("ENV", "production")
if ENV == "test":
    SQLALCHEMY_DATABSE_URL = os.getenv("DATA_BASE_TEST_URL")
else:
    SQLALCHEMY_DATABSE_URL = os.getenv("DATA_BASE_URL")

engine = create_engine(SQLALCHEMY_DATABSE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
