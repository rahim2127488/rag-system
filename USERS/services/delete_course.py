
def delete_course(course_id, db):
    
    connection = db
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM courses 
                    
                   WHERE course__id = (%s)
                   
                   """, course_id)
    
    connection.commit()
    cursor.close()