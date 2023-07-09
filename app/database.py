import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.environ['PGUSER']
password = os.environ['PGPASSWORD']
server = os.environ['PGHOST']
port = os.environ['PGPORT']
db = os.environ['PGDATABASE']

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{server}:{port}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
