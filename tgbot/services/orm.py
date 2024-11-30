from infrastructure.database.models import Base
from infrastructure.database.setup import create_my_engine
from tgbot import config
from tgbot.config import load_config


config = load_config(".env")
engine = create_my_engine(
        config.db,
        echo=True,
    )


class AsyncORM:
    """
    checkfirst=True: This flag tells SQLAlchemy to verify the existence of each table before trying to create it.
    If the table already exists, it will not attempt to recreate it.

    conn.run_sync: Allows running synchronous create_all within the asynchronous context provided by async with engine.begin().
    """
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            # Ensures only non-existent tables are created
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
