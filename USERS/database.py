import psycopg2
from SHARED.config import settings

def setup_database():
    
    url = f"postgresql://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_name}"
    db = psycopg2.connect(url)

    cursor = db.cursor()
        
    cursor.execute("""CREATE TABLE IF NOT EXISTS credentials(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL 
        )
        """)
    
    db.close()
    db.commit()
    cursor.close()

