import os
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), os.environ.get("DB_HOST"), os.environ.get("DB_PORT"), os.environ.get("DB_NAME"))
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()
Base.prepare(autoload_with=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()