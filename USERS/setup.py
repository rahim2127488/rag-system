import psycopg2
from SHARED.config import settings
##from INGESTION.ingest import course_name
##from INGESTION.ingest import course_code



def setup_database():
    
    url = f"postgresql://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_name}"
    db = psycopg2.connect(url)

    cursor = db.cursor()
        
    cursor.execute("""CREATE TABLE IF NOT EXISTS credentials(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_metadata(
        user_id INTEGER UNIQUE REFERENCES credentials(id),
        major TEXT,
        year int
        )
        """)
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS courses(
        course_id TEXT PRIMARY KEY,
        course_name TEXT NOT NULL
    )
                   
        """)
    
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS user_courses(
        user_id_ INTEGER REFERENCES credentials(id),
        course_id TEXT REFERENCES courses(course_id),
        progress TEXT DEFAULT 'not_started'
                CHECK (progress IN ('not_started', 'in_progress', 'completed')),
                UNIQUE(user_id_, course_id)
        )
       """)
    
    db.commit()
    cursor.close()
    db.close()

if __name__  == "__main__":
    setup_database()