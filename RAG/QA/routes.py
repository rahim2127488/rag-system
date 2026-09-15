from fastapi import APIRouter, Depends
from RAG.QA.models import QARequest
from RAG.QA.services.qa_retriever import qa_retrieve
from SHARED.dependencies import get_collection as collection
from SHARED.embeddings import generate_embedding

router = APIRouter()

@router.post("/qa")
def qa(req: QARequest, collec= Depends(collection)):
    embedding = generate_embedding(req.question)
    return qa_retrieve(
       collec,
       embedding,
       req.course,
       req.lesson,
       )