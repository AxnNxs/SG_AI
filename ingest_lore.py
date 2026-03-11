import asyncio
from db_manager import AsyncSessionLocal
from models import LoreChunk
from embedder import EmbedderService

async def carica_memoria():
    embedder = EmbedderService()
    
    # Leggiamo il tuo file di testo
    try:
        with open('background.txt', 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print("Errore: background non trovato")
        return

    # Dividiamo il testo in paragrafi per una ricerca più precisa
    chunks = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    
    print(f"Sto elaborando {len(chunks)} frammenti di background...")

    async with AsyncSessionLocal() as session:
        async with session.begin():
            for content in chunks:
                vector = embedder.generate_vector(content)
                nuovo_pezzo = LoreChunk(content=content, embedding=vector)
                session.add(nuovo_pezzo)
    
    print("✨ Memoria di sistema caricata con successo!")

if __name__ == "__main__":
    asyncio.run(carica_memoria())