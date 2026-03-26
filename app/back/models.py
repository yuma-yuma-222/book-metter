from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    # 1対多: 1人のユーザーは複数の本を持つ
    books = relationship("Book", back_populates="owner")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    total_pages = Column(Integer)
    target_date = Column(String)  # ISO形式の文字列で保存
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="books")
    # 1対多: 1冊の本には複数の進捗ログがある
    progress_logs = relationship("ProgressLog", back_populates="book")

class ProgressLog(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))
    start_page = Column(Integer)  
    end_page = Column(Integer)    
    memo = Column(String, nullable=True)

    book = relationship("Book", back_populates="progress_logs")