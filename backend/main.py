"""GabonEdu Campus - Backend FastAPI pour CUK/USTM"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import init_db, get_db
from .routers import auth, etudiants, filieres, notes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="GabonEdu Campus API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(etudiants.router, prefix="/api/v1/etudiants", tags=["Étudiants"])
app.include_router(filieres.router, prefix="/api/v1/filieres", tags=["Filières"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Notes"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "gabon_edu_backend"}
