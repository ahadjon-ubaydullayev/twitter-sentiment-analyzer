import asyncio
from app.database import engine
from app.models import Base

async def init_models():
    async with engine.begin() as conn:
        # Drop all tables (if needed)
        # await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_models())
