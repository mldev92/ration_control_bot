from sqlalchemy import select, delete, insert, DateTime, desc
from sqlalchemy.dialects.postgresql import insert
from infrastructure.database.models import Receipt
from infrastructure.database.repo.base import BaseRepo


class ReceiptRepo(BaseRepo):
    """
    This class will handle operations for the Receipt model, such as creating a receipt and associating it with a
    user. We'll also add methods for retrieving receipts and handling updates.
    """
    async def get_or_create_receipt(
            self,
            user_id: int,
            store_name: str,
            receipt_data: dict,
            purchased_at: DateTime
    ):
        """
        This method creates a new receipt or updates the existing one if a conflict occurs. It checks for conflict
        based on the user_id and purchased_at.
        """
        # Try to insert the receipt or update if it already exists
        insert_stmt = (
            insert(Receipt)
            .values(
                user_id=user_id,
                store_name=store_name,
                receipt_data=receipt_data,
                purchased_at=purchased_at
            )
            .on_conflict_do_update(
                index_elements=[Receipt.purchased_at, Receipt.user_id],
                set_=dict(
                    receipt_data=receipt_data,
                    store_name=store_name,
                ),
            )
            .returning(Receipt)
        )
        result = await self.session.execute(insert_stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_receipt_by_user_id(self, user_id: int):
        # Retrieve all receipts for a given user_id
        result = await self.session.execute(
            select(Receipt).filter_by(user_id=user_id).order_by(desc(Receipt.purchased_at))
        )
        return result.scalars().all()

    async def get_receipt_by_id(self, receipt_id: int):
        # Retrieve a specific receipt by its ID
        result = await self.session.execute(
            select(Receipt).filter_by(receipt_id=receipt_id)
        )
        return result.scalar_one_or_none()

    async def delete_receipt(self, receipt_id: int):
        """
        Deletes a receipt by its ID.
        """
        delete_stmt = delete(Receipt).where(Receipt.receipt_id == receipt_id)
        await self.session.execute(delete_stmt)
        await self.session.commit()
