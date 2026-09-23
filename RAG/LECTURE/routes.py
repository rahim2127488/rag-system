from fastapi import APIRouter, Depends
from RAG.LECTURE.schemas import LectureRequest
from RAG.LECTURE.services.lecture_retriever import lecture_retrieve
from SHARED.dependencies import get_collection as collection

router = APIRouter()

@router.post("/lecture")
def lecture(req: LectureRequest, collec = Depends(collection)):
    return lecture_retrieve(
        collec,
        req.course,
        req.lesson,
        req.concept
        )
    
    