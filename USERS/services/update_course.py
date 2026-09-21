from fastapi import HTTPException
def update_course(course_id,course_name,db):
    
    connection = db
    cursor = connection.cursor()
    try:
        cursor.execute("""UPDATE courses SET course_name = %s 
                   WHERE course_id = %s
                   RETURNING course_id
                   """, (course_name, course_id,))
        updates = cursor.fetchone()
        connection.commit()
    except updates is None:
        raise HTTPException(404)
    finally:
        cursor.close()
        