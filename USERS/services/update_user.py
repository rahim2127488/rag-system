import bcrypt
from fastapi import HTTPException

def update_user(user_id, name, email, password, major, year, db):
    
    connection = db
    cursor = connection.cursor()
    
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    cursor.execute("""UPDATE credentials SET name = %s, email = %s, password_hash = %s 
               WHERE id = %s
               RETURNING id
                """, (name, email, password_hash, user_id,))
    
    updates = cursor.fetchone()
    if updates is None:
        raise HTTPException(404)
      
    
    cursor.execute("""UPDATE user_metadata SET major = %s, year = %s
                  WHERE user_id = %s
                   """, (major, year, user_id,))
    connection.commit()  
    cursor.close()