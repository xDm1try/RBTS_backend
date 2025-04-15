from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# postgresql://admin:password@db:5432/battery_db
# postgres://postgres:password@localhost/postgres
DB_USER = os.getenv("DB_USER", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_NAME = os.getenv("DB_NAME", None)

assert DB_NAME and DB_PASS and DB_USER, "DB env is None"
print(f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}")
# engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}")
engine = create_engine(f"postgresql://postgres:password@localhost:5432/postgres")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
