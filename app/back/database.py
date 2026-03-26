from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# instanceフォルダ内にDBを作成する設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./instance/reading_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DBセッションを取得するための依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()