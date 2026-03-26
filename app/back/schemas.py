from pydantic import BaseModel, computed_field
from typing import List, Optional

# --- Progress (進捗ログ) ---
class ProgressBase(BaseModel):
    date: str
    start_page: int
    end_page: int
    memo: Optional[str] = None

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True

# --- Book (本) ---
class BookBase(BaseModel):
    title: str
    total_pages: int
    target_date: str

class BookCreate(BookBase):
    user_id: int

class Book(BookBase):
    id: int
    user_id: int
    progress_logs: List[Progress] = []

    # ★ 追加：APIがBookを返す時に、自動で「実質の合計ページ」を計算して含める
    @computed_field
    def total_read_pages(self) -> int:
        from .crud import calculate_total_progress
        return calculate_total_progress(self.progress_logs)

    class Config:
        from_attributes = True

# --- User (ユーザー) ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True