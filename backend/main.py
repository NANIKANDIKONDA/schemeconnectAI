import os
import sys

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import health, chat, schemes
from backend.rag.vector_store import index_schemes
from backend.api.routes.chat import get_all_schemes

# Initialize FastAPI App
app = FastAPI(
    title="SchemeConnect AI",
    description="AI-powered Government Scheme Eligibility Assistant",
    version="1.0.0"
)

# CORS middleware
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router)
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(schemes.router, prefix="/api", tags=["schemes"])

@app.on_event("startup")
async def startup_event():
    # Load and index schemes into vector database on startup
    print("Loading schemes and indexing into vector store...")
    schemes = get_all_schemes()
    index_schemes(schemes)
    print(f"Successfully loaded and indexed {len(schemes)} schemes.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
