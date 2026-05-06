"""GabonEdu Campus - Backend FastAPI pour CUK/USTM"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import database
from routers import auth, administration, vie_etudiante, finances, sync, etudiants, pedagogie, recherche

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
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
app.include_router(administration.router, prefix="/api/v1/administration", tags=["Administration"])
app.include_router(vie_etudiante.router, prefix="/api/v1/vie-etudiante", tags=["Vie Étudiante"])
app.include_router(finances.router, prefix="/api/v1/finances", tags=["Finances"])
app.include_router(sync.router, prefix="/api/v1/sync", tags=["Sync"])
app.include_router(etudiants.router, prefix="/api/v1/etudiants", tags=["Étudiants"])
app.include_router(pedagogie.router, prefix="/api/v1/pedagogie", tags=["Pédagogie"])
app.include_router(recherche.router, prefix="/api/v1/recherche", tags=["Recherche"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "gabon_edu_backend"}
