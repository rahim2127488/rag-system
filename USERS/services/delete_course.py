
def delete_course(course_id, db):
    
    connection = db
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM courses 
                    
                   WHERE course_id = (%s)
                   
                   """, course_id,)
    
    connection.commit()
    cursor.close()