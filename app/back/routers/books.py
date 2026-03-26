from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database, models
router = APIRouter(
    prefix="/api/books",
    tags=["books"]
)

@router.post("/{book_id}/progress", response_model=schemas.Progress)
def create_progress(book_id: int, progress: schemas.ProgressCreate, db: Session = Depends(database.get_db)):
    """② 進捗入力: 特定の本に対して、読んだページ数とメモを記録します"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.create_book_progress(db=db, progress=progress, book_id=book_id)

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    """③ Book登録: ユーザーIDを指定して新しい本を登録します"""
    # ユーザーが存在するかチェック
    db_user = crud.get_user(db, user_id=book.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_book(db=db, book=book)

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    """⑤ Book削除: IDを指定して本を削除します"""
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book '{db_book.title}' deleted successfully"}

# --- ここに「特定のユーザーの本一覧」を取得するエンドポイントを追加 ---
# usersルーターに入れても良いですが、管理上こちらに書く手法もあります
@router.get("/user/{user_id}", response_model=List[schemas.Book])
def read_user_books(user_id: int, db: Session = Depends(database.get_db)):
    """④ Book取得: 特定のユーザーが持っている本の一覧を取得します"""
    return crud.get_user_books(db, user_id=user_id)