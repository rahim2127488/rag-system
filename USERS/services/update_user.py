import bcrypt
from fastapi import HTTPException

def update_user(user_id, name, email, password, major, year, db):
    
    connection = db
    cursor = connection.cursor()
    
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    cursor.execute("""UPDATE credentials SET name = %s, email = %s, password = %s 
               WHERE user_id = %s
               RETURNING user_id
                """, (name, email, password_hash, user_id,))
    
    updates = cursor.fetchone()
    if updates is None:
        raise HTTPException(404)
    connection.commit()    
    
    cursor.execute("""UPDATE user_metadata SET major = %s, year = %s
                  WHERE user_id = %s
                   """, (major, year,))

    cursor.close()