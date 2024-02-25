from sqlalchemy import create_engine, Column, Integer, String, DateTime
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class FileVector(Base):
    __tablename__ = 'file_vector'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    file_path = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
