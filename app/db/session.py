from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
