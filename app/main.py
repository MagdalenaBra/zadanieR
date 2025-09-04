from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from .database import Base, engine, get_db
from .models import Book
from .schemas import BookCreate, BookOut, StatusUpdate
from typing import List
from datetime import datetime
import uvicorn

app = FastAPI(title="Library API", version="1.0.0")

# Create DB schema on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    # Check uniqueness
    exists = db.get(Book, payload.serial_number)
    if exists is not None:
        raise HTTPException(status_code=409, detail="Książka o podanym numerze seryjnym już istnieje.")
    book = Book(
        serial_number=payload.serial_number,
        title=payload.title.strip(),
        author=payload.author.strip(),
        is_borrowed=False,
        borrowed_at=None,
        borrower_card=None
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.get("/books", response_model=List[BookOut])
def list_books(db: Session = Depends(get_db)):
    result = db.execute(select(Book).order_by(Book.serial_number))
    return [row[0] for row in result.all()]

@app.delete("/books/{serial_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(serial_number: str, db: Session = Depends(get_db)):
    book = db.get(Book, serial_number)
    if book is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki.")
    db.delete(book)
    db.commit()
    return None

@app.patch("/books/{serial_number}/status", response_model=BookOut)
def update_status(serial_number: str, update: StatusUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, serial_number)
    if book is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki.")
    if update.action == "borrow":
        if book.is_borrowed:
            raise HTTPException(status_code=409, detail="Książka jest już wypożyczona.")
        if not update.borrower_card:
            raise HTTPException(status_code=422, detail="Wymagany numer karty wypożyczającego (6 cyfr).")
        book.is_borrowed = True
        book.borrower_card = update.borrower_card
        book.borrowed_at = update.borrowed_at
    elif update.action == "return":
        if not book.is_borrowed:
            # Idempotent: return OK with unchanged state
            pass
        book.is_borrowed = False
        book.borrower_card = None
        book.borrowed_at = None
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
