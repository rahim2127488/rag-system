from pydantic import BaseModel

class UserCreate(BaseModel):
    name : str
    email : str 
    password : str
    major : str
    year : int
    
class CourseUpdate(BaseModel):
    course_id_update : str
    course_name_update : str
    
class UserUpdate(BaseModel):
    name_update : str
    email_update : str
    password_update : str
    major_update : str
    year_update : int