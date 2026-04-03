from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

app = FastAPI(title="Fast Coffee Professional API")

# CORS cho frontend local / deployed apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,  # nếu cần tài nguyên bảo mật thì đổi thành ['http://localhost:3000']
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Đăng ký Version 1
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "Online", "v1_docs": "/api/v1/docs"}