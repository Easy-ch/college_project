from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.models import Base

async_engine = create_async_engine(
    url             =  DATABASE_URL,
    pool_size       =  10,
    max_overflow    =  5,
    echo_pool       =  True,
)


AsyncSessionLocal = sessionmaker(
    bind             = async_engine,
    class_           = AsyncSession,
    expire_on_commit = False,
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


from sqlalchemy.ext.asyncio import AsyncEngine

async def run_migrations_online():
    connectable = async_engine

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

async def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=Base)

    with context.begin_transaction():
        context.run_migrations()
