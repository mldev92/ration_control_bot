from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, Text, JSON, Float, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import BIGINT

from infrastructure.database.models import Base
from infrastructure.database.models.base import TimestampMixin, TableNameMixin


class Product(Base, TimestampMixin, TableNameMixin):
    """
    product_id: Primary key with auto-increment.

    receipt_id: Foreign key referencing Receipt.receipt_id with cascade delete (ondelete='CASCADE').

    product_name: Required field with a max length of 255 characters.

    Nullable fields: quantity, weight, unit, and calories for flexibility in capturing varying product details.

    predicted_category: Optional, to allow for predicted classifications.

    created_at: Automatically set to the current timestamp.

    Relationships:
        User → Receipt (User has receipts attribute via back_populates).
        Receipt → Product (Receipt has products attribute via back_populates).

    Cascade Options:
        Deleting a user cascades to their receipts.
        Deleting a receipt cascades to its products.
    """
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey('receipts.receipt_id', ondelete='CASCADE'), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)
    calories: Mapped[float] = mapped_column(Float, nullable=True)
    predicted_category: Mapped[str] = mapped_column(String(128), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relationship to Receipt
    receipt = relationship("Receipt", back_populates="products")

    # # Add composite unique constraint
    # __table_args__ = (
    #     UniqueConstraint('receipt_id', 'product_name', name='uq_receipt_id_product_name'),
    # )