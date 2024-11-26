import json
from passlib.context import CryptContext

def load_services():
    with open("data/popular_services.json", "r", encoding="utf-8") as file:
        return json.load(file)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
