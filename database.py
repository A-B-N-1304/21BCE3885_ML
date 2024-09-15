from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    request_count = Column(Integer, default=1)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user_if_not_exists(db: Session, user_id: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        new_user = User(user_id=user_id, request_count=1)
        db.add(new_user)
        db.commit()

def increment_user_request_count(db: Session, user_id: str) -> int:
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.request_count += 1
        db.commit()
        return user.request_count
    return 0
