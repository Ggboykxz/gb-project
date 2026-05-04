"""Configuration de la base de données SQLite avec SQLCipher"""
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Chemin de la base de données dans AppData
if os.name == 'nt':  # Windows
    APP_DATA = Path(os.environ.get('APPDATA', '')) / 'gabon_edu'
else:  # macOS/Linux
    APP_DATA = Path.home() / '.local' / 'share' / 'gabon_edu'

APP_DATA.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite+aiosqlite:///{APP_DATA / 'campus.db'}"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_db():
    """Initialise la base de données"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Dépendance FastAPI pour obtenir une session DB"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
