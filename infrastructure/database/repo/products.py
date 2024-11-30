from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Product
from infrastructure.database.repo.base import BaseRepo


class ProductRepo(BaseRepo):
    """This class will handle operations for the Product model. Since you will be updating the product with additional
    information like weight, unit, calories, and predicted category later, I've added methods to insert or update
    products as well.
    """
    async def get_or_create_product(
        self,
        receipt_id: int,
        product_name: str,
        quantity: Optional[float] = None,
        weight: Optional[float] = None,
        unit: Optional[str] = None,
        calories: Optional[float] = None,
        predicted_category: Optional[str] = None,
    ):
        # Insert or update the product in the database
        insert_stmt = (
            insert(Product)
            .values(
                receipt_id=receipt_id,
                product_name=product_name,
                quantity=quantity,
                weight=weight,
                unit=unit,
                calories=calories,
                predicted_category=predicted_category,
            )
            # .on_conflict_do_update(
            #     index_elements=[Product.receipt_id, Product.product_name],
            #     set_={
            #         "quantity": quantity,
            #         "weight": weight,
            #         "unit": unit,
            #         "calories": calories,
            #         "predicted_category": predicted_category,
            #     },
            # )
            .returning(Product)
        )
        result = await self.session.execute(insert_stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_products_by_receipt_id(self, receipt_id: int):
        # Retrieve all products for a given receipt_id
        result = await self.session.execute(
            select(Product).filter_by(receipt_id=receipt_id)
        )
        return result.scalars().all()

    async def get_product_by_id(self, product_id: int):
        # Retrieve a specific product by its ID
        result = await self.session.execute(
            select(Product).filter_by(product_id=product_id)
        )
        return result.scalar_one_or_none()

    async def update_product_details(
        self,
        product_id: int,
        weight: Optional[float] = None,
        unit: Optional[str] = None,
        calories: Optional[float] = None,
        predicted_category: Optional[str] = None,
    ):
        # Update specific product details
        update_stmt = (
            update(Product)
            .where(Product.product_id == product_id)
            .values(
                weight=weight,
                unit=unit,
                calories=calories,
                predicted_category=predicted_category,
            )
            .returning(Product)
        )
        result = await self.session.execute(update_stmt)
        await self.session.commit()
        return result.scalar_one()
