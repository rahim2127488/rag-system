from pydantic import BaseModel

class QARequest(BaseModel):
    course: str
    lesson: str
    question : str
    
class Chunk(BaseModel):
    course: str
    lesson: str
    concept: str
    chunk_index: int
    text: str