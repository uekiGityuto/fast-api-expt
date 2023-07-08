import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.getenv('PGUSER')
password = os.getenv('PGPASSWORD')
server = os.getenv('PGHOST')
port = os.getenv('PGPORT')
db = os.getenv('PGDATABASE')

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{server}:{port}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
