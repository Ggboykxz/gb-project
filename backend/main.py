import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routers import administration, vie_etudiante, finances

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🎓 GabonEdu Campus Backend starting...")
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 GabonEdu Campus Backend shutting down...")

app = FastAPI(
    title="GabonEdu Campus API",
    description="API pour la gestion académique des universités gabonaises",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "tauri://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(administration.router, prefix="/api/v1/administration", tags=["Administration"])
app.include_router(vie_etudiante.router, prefix="/api/v1/vie-etudiante", tags=["Vie Étudiante"])
app.include_router(finances.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "gabon-edu-campus-backend"}

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur GabonEdu Campus API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)
