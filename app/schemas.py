from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime, timezone

def _six_digit_str(v: str) -> str:
    if not isinstance(v, str):
        raise ValueError("Musi być łańcuchem znaków.")
    if len(v) != 6 or not v.isdigit():
        raise ValueError("Wymagane 6 cyfr.")
    return v

class BookCreate(BaseModel):
    serial_number: str = Field(..., description="Sześciocyfrowy numer seryjny (np. '012345')")
    title: str
    author: str

    @field_validator("serial_number")
    @classmethod
    def validate_serial(cls, v: str):
        return _six_digit_str(v)

class BookOut(BaseModel):
    serial_number: str
    title: str
    author: str
    is_borrowed: bool
    borrowed_at: Optional[datetime] = None
    borrower_card: Optional[str] = None

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    action: Literal["borrow", "return"]
    borrower_card: Optional[str] = None
    borrowed_at: Optional[datetime] = None

    @field_validator("borrower_card")
    @classmethod
    def validate_card(cls, v: Optional[str]):
        if v is None:
            return v
        return _six_digit_str(v)

    @field_validator("borrowed_at")
    @classmethod
    def default_borrowed_at(cls, v: Optional[datetime]):
        return v or datetime.now(timezone.utc)
