from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db import get_db
from models.models import User
from utils import hash_password, verify_password
from jwt_utils import verify_token, create_refresh_token, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from schemas.schemas import RegisterUser, TokenResponse
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy import select
from fastapi_mail import FastMail, MessageSchema
from config import *
import logging
from fastapi.security import OAuth2PasswordBearer

auth_reg_router = APIRouter()

@auth_reg_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUser, db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.email == user.email) | (User.username == user.username))
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email или username уже существует.",
        )
    
    new_user = User(
        email=user.email,
        username=user.username,
        password=hash_password(user.password),
    )
    try:
        db.add(new_user)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при сохранении пользователя."
        )

    token = serializer.dumps(user.email, salt="email-confirmation")

    confirmation_url = f"{SERVER_ADDRES}/confirm-email/{token}"
    logging.info(f"{confirmation_url}\n")

    message = MessageSchema(
        subject="Подтверждение регистрации",
        recipients=[user.email],
        body=f"Перейдите по ссылке для подтверждения: {confirmation_url}",
        subtype="plain",
    )

    fm = FastMail(email_config)
    await fm.send_message(message)

    return {"message": "Письмо с подтверждением отправлено"}


@auth_reg_router.get("/confirm-email/{token}")
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        email = serializer.loads(token, salt="email-confirmation", max_age=300)  # 5 минут
        
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден."
            )

        # Обновляем поле isAuthorized
        user.isAuthorized = True
        await db.commit()

        return {"message": f"Email {email} успешно подтвержден!"}

    except SignatureExpired:
        raise HTTPException(
            status_code=400,
            detail="Срок действия ссылки истек. Пожалуйста, запросите новую."
        )
    except BadSignature:
        raise HTTPException(
            status_code=400,
            detail="Недействительная ссылка подтверждения."
        )
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")
    return payload
    

@auth_reg_router.post("/login", response_model=TokenResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.username == form_data.username) | (User.email == form_data.username))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")

    if not user.isAuthorized:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email не подтвержден")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    print("Password match:", verify_password(form_data.password, user.password))

    return { "access_token": access_token,
             "refresh_token": refresh_token }


@auth_reg_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутствует refresh token")

    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный refresh token")

    query = select(User).where(User.username == payload["sub"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token}


@auth_reg_router.post("/verify-token")
async def verify_token_endpoint(token: str = Depends(oauth2_scheme)):
    """
    Эндпоинт для проверки валидности токена.
    Возвращает данные из токена, если он действителен.
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Недействительный или истёкший токен"
        )
    return {"message": "Токен действителен", "data": payload}


@auth_reg_router.get("/get_user_data")
async def protected_route(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user['sub'])
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user:
        return {
                    "email": user.email,
                    "username": user.username,
                    # "phone_number": user.phone_number
               }

    return {"message": f"Данные токена доступа неверны."}


# @auth_reg_router.get("/profile")
# async def profile(user: dict = Depends(get_current_user)):
    
#     return {"message": f"Профиль пользователя: {user['sub']}"}
