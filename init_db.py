from db_manager import engine
from models import Base
from sqlalchemy import text
import asyncio

async def init_database():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
        
if __name__ == "__main__":
    asyncio.run(init_database())