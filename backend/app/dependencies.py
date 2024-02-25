from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
