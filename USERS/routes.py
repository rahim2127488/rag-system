from SHARED.dependencies import get_user_db
from fastapi import APIRouter, Depends
from USERS.schemas import UserCreate
from USERS.schemas import UserUpdate
from USERS.schemas import CourseUpdate
from USERS.services.add_user import add_user
from USERS.services.delete_user import delete_user
from USERS.services.delete_course import delete_course
from USERS.services.update_user import update_user
from USERS.services.update_course import update_course

router = APIRouter()

@router.post("/users")
def create_user(req: UserCreate, db = Depends(get_user_db)):
    return add_user(
        req.name,
        req.email,
        req.password,
        req.major,
        req.year,
        db
        )
    
@router.delete("/users/{user_id}")
def remove_user(user_id: str, db = Depends(get_user_db)):
    return delete_user(user_id, db)

@router.delete("/courses/{course_id}")
def remove_course(course_id : str, db = Depends(get_user_db)):
    return delete_course(course_id, db)

@router.put("/user/{user_id}")
def update_user_info(user_id : str, req:UserUpdate, db = Depends(get_user_db)):
    return update_user(user_id, 
                         req.name,
                         req.email,
                         req.password,
                         req.major,
                         req.year,
                         db 
                         )

@router.put("/courses/{course_id}")
def update_course_info(course_id : str, req:CourseUpdate, db = Depends(get_user_db)):
    return update_course(course_id, 
                         req.course_name,
                         db 
                         )
    
