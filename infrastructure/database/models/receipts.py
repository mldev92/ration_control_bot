from sqlalchemy import (
    Integer, String, ForeignKey, JSON, DateTime, LargeBinary, UniqueConstraint
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import BIGINT

from infrastructure.database.models import Base
from infrastructure.database.models.base import TimestampMixin, TableNameMixin


class Receipt(Base, TimestampMixin, TableNameMixin):
    """
    receipt_id: Primary key with auto-increment.

    user_id: Foreign key referencing User.user_id with cascade delete (ondelete='CASCADE').

    store_name: Required field with a max length of 255 characters.

    receipt_data: Stored as JSON to accommodate receipt information.

    created_at: Automatically set to the current timestamp using func.now().

    Relationships:
        User → Receipt (User has receipts attribute via back_populates).
        Receipt → Product (Receipt has products attribute via back_populates).

    Cascade Options:
        Deleting a user cascades to their receipts.
        Deleting a receipt cascades to its products.
    """
    receipt_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    store_name: Mapped[str] = mapped_column(String(255), nullable=False)
    # receipt_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)  # Storing receipt data as bytes
    receipt_data: Mapped[dict] = mapped_column(JSON, nullable=False)  # Storing structured data as JSON
    purchased_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)  # Purchase date and time
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relationship to User
    user = relationship("User", back_populates="receipts")
    # Relationship to Products
    products = relationship("Product", back_populates="receipt", cascade="all, delete-orphan")

    # Add composite unique constraint
    __table_args__ = (
        UniqueConstraint('purchased_at', 'user_id', name='uq_purchased_at_user_id'),
    )