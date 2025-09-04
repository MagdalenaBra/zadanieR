from sqlalchemy import String, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from datetime import datetime
from typing import Optional

class Book(Base):
    __tablename__ = "books"

    # Serial number as string to preserve leading zeros; enforce 6-digit via constraint
    serial_number: Mapped[str] = mapped_column(String(6), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)

    is_borrowed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    borrowed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    borrower_card: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)

    __table_args__ = (
        CheckConstraint("char_length(serial_number) = 6", name="serial_number_len_6"),
        CheckConstraint("(borrower_card IS NULL) OR char_length(borrower_card) = 6", name="borrower_card_len_6"),
    )
