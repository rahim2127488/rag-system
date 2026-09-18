from SHARED.dependencies import get_user_db
from fastapi import APIRouter, Depends
from USERS.schemas import UserCreate
from USERS.services.add_user import add_user 

router = APIRouter()

@router.post("/users")
def add_user(req: UserCreate, db = Depends(get_user_db)):
    return add_user(
        req.name,
        req.email,
        req.password,
        db
        )