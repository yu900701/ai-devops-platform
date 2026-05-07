from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="AI DevOps Platform",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "AI DevOps Platform Running",
        "timestamp": datetime.now()
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/info")
def info():
    return {
        "app": "AI DevOps Platform",
        "version": "0.1.0",
        "service": "FastAPI Backend"
    }