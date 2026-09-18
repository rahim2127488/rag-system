from SHARED.dependencies import get_user_db
from fastapi import APIRouter, Depends
from USERS.schemas import UserCreate
from USERS.services.add_user import add_user 
from USERS.services.delete_user import delete_user 
from USERS.services.delete_course import delete_course 

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
def remove_user(user_id: int, db = Depends(get_user_db)):
    return delete_user(user_id, db)

@router.delete("/courses/{course_id}")
def remove_course(course_id : int, db = Depends(get_user_db)):
    return delete_course(course_id, db)