import chromadb
import psycopg2
from SHARED.config import settings


client = chromadb.PersistentClient(settings.chroma_path)

collection = client.get_or_create_collection(
    name= "course_chunks",
    metadata={"hnsw:space": "cosine"}
)

def get_collection():
    return collection



def get_user_db():
   
    url = f"postgresql://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_name}"
    connection = psycopg2.connect(url)
    try:
        yield connection
        
    finally:
        connection.close() 