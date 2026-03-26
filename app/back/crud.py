from sqlalchemy.orm import Session
from . import models, schemas


# --- User 操作 ---

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 本来はここでパスワードをハッシュ化します
    db_user = models.User(username=user.username, password_hash=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Book 操作 ---

def get_user_books(db: Session, user_id: int):
    return db.query(models.Book).filter(models.Book.user_id == user_id).all()

def create_user_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        total_pages=book.total_pages,
        target_date=book.target_date,
        user_id=book.user_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def create_book_progress(db: Session, progress: schemas.ProgressCreate, book_id: int):
    db_progress = models.ProgressLog(
        **progress.model_dump(),
        book_id=book_id
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def calculate_unique_pages(logs):
    """
    [[1, 30], [20, 40]] のようなログから、
    重複を除いたユニークな読了ページ数（この場合は 40ページ）を計算する
    """
    if not logs:
        return 0
    
    # 開始ページでソート
    intervals = sorted([(log.start_page, log.end_page) for log in logs])
    
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    
    # 統合された各区間の長さを合計
    # 例: [[1, 40]] なら 40 - 1 + 1 = 40ページ
    total = sum(end - start + 1 for start, end in merged)
    return total


def calculate_total_progress(logs):
    if not logs:
        return 0
    
    # 1. 開始ページでソート: [(1, 10), (30, 50)]
    intervals = sorted([(log.start_page, log.end_page) for log in logs])
    
    # 2. 重複する範囲をマージ
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1] + 1: 
            # 前の区間と繋がっていない場合（+1は1ページ単位の連続性を考慮）
            merged.append([start, end])
        else:
            # 重なっている、または連続している場合は末尾を伸ばす
            merged[-1][1] = max(merged[-1][1], end)
            
    # 3. 各区間の実質ページ数を合計
    # [1, 10] -> 10 - 1 + 1 = 10
    # [30, 50] -> 50 - 30 + 1 = 21
    # 合計: 31ページ
    total = sum(end - start + 1 for start, end in merged)
    return total