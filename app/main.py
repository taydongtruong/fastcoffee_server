from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="Fast Coffee Professional API")

# Đăng ký Version 1
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "Online", "v1_docs": "/api/v1/docs"}