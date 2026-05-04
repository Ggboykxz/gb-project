import os
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Database path - stored in AppData/Application Support
if os.name == 'nt':  # Windows
    app_data = os.environ.get('APPDATA', str(Path.home()))
    db_dir = Path(app_data) / "gabon_edu"
else:  # macOS/Linux
    db_dir = Path.home() / ".gabon_edu"

db_dir.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite+aiosqlite:///{db_dir / 'campus.db'}"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def init_db():
    """Initialize database and create tables"""
    async with async_engine.begin() as conn:
        # Import all models to ensure they're registered with Base
        from models import administration, vie_etudiante, finances, security
        
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """Dependency for getting async database session"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_async_session() -> AsyncSession:
    """Get async session for scripts"""
    return async_session()
