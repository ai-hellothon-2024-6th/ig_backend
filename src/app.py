# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import *

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(info_router, prefix="/info")
app.include_router(media_router, prefix="/media")
app.include_router(emotional_router, prefix="/comment/emotional")
app.include_router(motivational_router, prefix="/comment/motivational")
app.include_router(comment_router, prefix="/comment")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용 (보안을 위해 적절히 설정 필요)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용 (필요한 메소드만 허용하도록 설정 권장)
    allow_headers=["*"],  # 모든 헤더 허용 (필요한 헤더만 허용하도록 설정 권장)
)
