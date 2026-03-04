from database import engine, Base
from sqlalchemy import text
import asyncio

async def init_database():
    async with engine.begin() as conn:
        pass

if __name__ == "__main__":
    asyncio.run(init_database())