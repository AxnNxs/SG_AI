from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    # L'ID che arriva dalla piattaforma (es. "ig_123456")
    external_id = Column(String, unique=True, nullable=False, index=True)
    platform = Column(String, nullable=False) # "instagram", "onlyfans", etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relazione con i messaggi
    messages = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False) # "user" o "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="messages")

class LoreChunk(Base):
    __tablename__ = "lore_chunks"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    # 768 è la dimensione standard per molti modelli di embedding (es. Mistral o BERT)
    embedding = Column(Vector(768))

    # Crea un indice HNSW (Hierarchical Navigable Small World). 
    # È l'algoritmo più veloce nel 2026 per cercare vettori.
    __table_args__ = (
        Index(
            'lore_chunks_embedding_idx', 
            embedding, 
            postgresql_using='hnsw', 
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'embedding': 'vector_cosine_ops'}
        ),
    )

    def to_context_string(self) -> str:
        return f"[Background Fragment]: {self.content}"
        #...

    @staticmethod
    def validate_embedding(vector: list[float]) -> bool:
        if len(vector) != 768:
            raise ValueError(f"Vector dimension error: expected 768, received {len(vector)}")
        #pass


