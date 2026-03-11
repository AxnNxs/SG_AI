from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from pgvector.sqlalchemy import Vector # O L2Distance
from models import LoreChunk

# L'URL punta al container 'db' definito nel docker-compose
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/ia_db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Funzione per ottenere la sessione DB in FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def search_relevant_context(user_query, db_session, embedder):
    # 1. Trasforma la domanda dell'utente in vettore
    query_vector = embedder.generate_vector(user_query)
    
    # 2. Cerca nel DB usando la distanza coseno (più piccola = più simile)
    stmt = (
        select(LoreChunk)
        .order_by(LoreChunk.embedding.cosine_distance(query_vector))
        .limit(3) # Prendiamo i 3 frammenti più pertinenti
    )
    
    result = await db_session.execute(stmt)
    chunks = result.scalars().all()
    
    # 3. Unisci i testi trovati
    return "\n\n".join([c.content for c in chunks])

async def save_to_memory(content, embedding, session):
    new_chunk = LoreChunk(content=content, embedding=embedding)
    session.add(new_chunk)
    await session.commit()