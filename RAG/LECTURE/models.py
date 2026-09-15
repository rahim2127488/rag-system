from pydantic import BaseModel

class LectureRequest(BaseModel):
    course: str
    lesson: str
    concept: str