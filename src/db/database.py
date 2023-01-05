from fastapi import Depends
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv() # take invironment variables from .env

POSTGRES = {
  "user": os.getenv("PGUSER"),
  "pw":   os.getenv("PGPASSWORD"),
  "host": os.getenv("PGHOST"),
  "port": os.getenv("PGPORT"),
  "db":   os.getenv("PGDATABASE"),
}

SQLALCHEMY_DATABASE_URL="postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
