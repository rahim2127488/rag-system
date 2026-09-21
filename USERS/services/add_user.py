import bcrypt
def add_user(name, email, password, major, year, db):
    
    connection = db
    cursor = connection.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cursor.execute("""INSERT INTO credentials (name, email, password_hash) 
                   VALUES (%s , %s, %s)
                   RETURNING id
                   """, (name, email, password_hash,))
    user_id = cursor.fetchone()[0]
    cursor.execute("""INSERT INTO user_metadata (user_id, major, year) 
                       VALUES (%s , %s, %s)
                       """, (user_id, major, year,))
    
    connection.commit()
    cursor.close()