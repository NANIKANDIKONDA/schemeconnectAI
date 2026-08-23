from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SchemeConnect AI",
        "version": "1.0.0"
    }

@router.get("/")
def root():
    return {
        "message": "Welcome to SchemeConnect AI API",
        "docs": "/docs"
    }
