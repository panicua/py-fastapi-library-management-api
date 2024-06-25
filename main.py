from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db, author)
    return db_author


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_author_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/author/{author_id}", response_model=list[schemas.Book])
def read_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author_id(db, author_id=author_id)
    return books
