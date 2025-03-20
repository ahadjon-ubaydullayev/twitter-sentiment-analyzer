import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")  # e.g., "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency for FastAPI endpoints
async def get_db():
    async with async_session() as session:
        yield session
