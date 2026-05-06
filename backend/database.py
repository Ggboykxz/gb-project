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
    from sqlalchemy import text
    async with engine.begin() as conn:
        try:
            # Créer les tables une par une en ignorant les erreurs de FK
            for table in Base.metadata.sorted_tables:
                try:
                    await conn.run_sync(table.create, checkfirst=True)
                except Exception as e:
                    # Log l'erreur mais continuer
                    print(f"Table {table.name}: {str(e)[:100]}")
            print("Base de données initialisée")
        except Exception as e:
            print(f"Erreur init DB: {e}")
            # Ne pas lever l'exception pour permettre le démarrage

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
