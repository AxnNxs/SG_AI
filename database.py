from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# L'URL punta al container 'db' definito nel docker-compose
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/ia_db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Funzione per ottenere la sessione DB in FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
