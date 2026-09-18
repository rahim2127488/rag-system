from fastapi import FastAPI
from RAG.LECTURE.routes import router as lecture_router
from RAG.QA.routes import router as qa_router
from USERS.routes import router as user_router

app = FastAPI()
app.include_router(lecture_router)
app.include_router(qa_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"status": "ok"}
