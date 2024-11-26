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













# import asyncpg
# from config import DATABASE_URL
# from passlib.context import CryptContext

# from contextlib import asynccontextmanager
# from models.models import User

# pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


# async def hash_password(password: str):
#     return pwd_context.hash(password)


# async def connect_to_db():
#     conn = await asyncpg.connect(DATABASE_URL) 
#     await create_table_user(conn)
#     return conn

    

# async def create_table_user(conn):
#     async with conn.acquire() as conn:
#         await conn.execute(
#             """ CREATE TABLE IF NOT EXISTS user(
#                 id SERIAL PRIMARY KEY,
#                 email varchar NULL,
#                 username varchar NULL,
#                 password varchar NOT NULL;
#             """)


# async def add_user(conn, user: User):
#     await hash_password(user.password)
#     async with conn.acquire() as conn:
#         try:
#             await conn.execute(
#                 """
#                 INSERT INTO users (email, username, password)
#                 VALUES ($1, $2, $3)
#                 """)
#         except Exception as e:
#             return e
        

# async def get_user(username, conn):
#     async with conn.acquire() as conn:
#         query = """
#             SELECT * FROM user WHERE username = $1;
#             """
#         return conn.fetchrow(query, username)

