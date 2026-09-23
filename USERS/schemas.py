from pydantic import BaseModel

class UserCreate(BaseModel):
    name : str
    email : str 
    password : str
    major : str
    year : int
    
class CourseUpdate(BaseModel):
    course_name : str
    
class UserUpdate(BaseModel):
    name : str
    email : str
    password : str
    major : str
    year : int