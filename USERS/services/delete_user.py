
def delete_user(id, db):
    
    connection = db
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM user_courses 
                       WHERE user_id = (%s)
                       """, (id,))
    
    cursor.execute("""DELETE FROM user_metadata 
                       WHERE user_id = (%s)
                       """, (id,))
    
    cursor.execute("""DELETE FROM credentials 
                       WHERE id = (%s)
                       """, (id,))

    connection.commit()
    cursor.close()
        