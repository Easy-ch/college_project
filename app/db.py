import asyncpg
from config import DATABASE_URL
from passlib.context import CryptContext

from contextlib import asynccontextmanager
from models.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


async def hash_password(password: str):
    return pwd_context.hash(password)


async def connect_to_db():
    conn = await asyncpg.connect(DATABASE_URL) 
    await create_table_user(conn)
    return conn

    

async def create_table_user(conn):
    async with conn.acquire() as conn:
        await conn.execute(
            """ CREATE TABLE IF NOT EXISTS user(
                id SERIAL PRIMARY KEY,
                email varchar NULL,
                username varchar NULL,
                password varchar NOT NULL;
            """)


async def add_user(conn, user: User):
    await hash_password(user.password)
    async with conn.acquire() as conn:
        try:
            await conn.execute(
                """
                INSERT INTO users (email, username, password)
                VALUES ($1, $2, $3)
                """)
        except Exception as e:
            return e
        

async def get_user(username, conn):
    async with conn.acquire() as conn:
        query = """
            SELECT * FROM user WHERE username = $1;
            """
        return conn.fetchrow(query, username)

