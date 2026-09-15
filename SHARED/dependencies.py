import chromadb
from SHARED.config import settings

client = chromadb.PersistentClient(settings.chroma_path)

collection = client.get_or_create_collection(
    name= "course_chunks",
    metadata={"hnsw:space": "cosine"}
)

def get_collection():
    return collection

