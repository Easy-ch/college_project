from fastapi import APIRouter, Depends, HTTPException, status, Request,Form
from fastapi.responses import JSONResponse,FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from db import get_db
from models.models import User
from utils import hash_password, verify_password, send_registration_email,send_reset_email
from jwt_utils import verify_token, create_refresh_token, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from schemas.schemas import RegisterUser,ResetPasswordModel
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy import select
from config import *
from fastapi.security import OAuth2PasswordBearer
from config import REFRESH_TOKEN_EXPIRE_DAYS

auth_reg_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
templates = Jinja2Templates(directory='templates')

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{ "message": "Недействительный токен" }])
    return payload


@auth_reg_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUser, db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.email == user.email) | (User.username == user.username))
    result = await db.execute(query)
    existing_users = result.scalars().all()
    if existing_users:
        for existing_user in existing_users:
            if not existing_user.isAuthorized:
                token = serializer.dumps(user.email, salt="email-confirmation")
                confirmation_url = f"{SERVER_ADDRES}/confirm-email?token={token}"
                await send_registration_email(user.email, confirmation_url)
                await db.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=[{ "message": "Пользователь не подтвержден, ссылка для повторного подтверждения отправлена на почту" }])
    else:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=[{ "message": "Пользователь с таким email или username уже существует" }])

    token = serializer.dumps(user.email, salt="email-confirmation")

    confirmation_url = f"{SERVER_ADDRES}/confirm-email?token={token}"

    await send_registration_email(user.email, confirmation_url)
    
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
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=[{ "message": "Ошибка при сохранении пользователя." }])

    return JSONResponse({
        "message": f"Подтвердите регистрацию по ссылке, отправленной по электронной почте"
    })


@auth_reg_router.get("/confirm-email")
async def confirm_email(token: str,request: Request, db: AsyncSession = Depends(get_db)):
    try:
        email = serializer.loads(token, salt="email-confirmation", max_age=300)  # 5 минут
        
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=[{ "message": "Пользователь не найден."}])

        user.isAuthorized = True
        await db.commit()

        # return JSONResponse(
        #     {"message": "Email успешно подтверждён!"},
        #     status_code=status.HTTP_200_OK
        # )

    except SignatureExpired:
        raise HTTPException(status_code=400,
                            detail=[{ "message": "Срок действия ссылки истек. Пожалуйста, запросите новую." }])
    except BadSignature:    
        raise HTTPException(status_code=400,
                            detail=[{ "message": "Недействительная ссылка подтверждения." }])

    
    return templates.TemplateResponse('confirm-email.html',{"request":request,"message": "Email успешно подтверждён"})


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{ "message": "Недействительный токен" }])
    return payload
    

@auth_reg_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.username == form_data.username) | (User.email == form_data.username))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{ "message": "Неверные учетные данные" }])

    if not user.isAuthorized:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=[{ "message": "Email не подтвержден" }])

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    response = JSONResponse({
        "access_token": access_token
    })

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,   # Используйте True для HTTPS
        samesite="Strict",
        expires=(datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    )

    return response


@auth_reg_router.post("/refresh")
async def refresh_token(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{ "message": "Отсутствует refresh token" }])

    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{ "message": "Недействительный refresh token" }])

    query = select(User).where(User.username == payload["sub"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{ "message": "Пользователь не найден" }])

    access_token = create_access_token( {"sub": user.username} )
    return { "access_token": access_token }


@auth_reg_router.get("/get_user_data")
async def protected_route(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.username == user['sub']) | (User.email == user['sub']))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user:
        return JSONResponse({
            "email": user.email,
            "username": user.username,
            "phone":user.phone_number or "Не указано"
        })

    return JSONResponse({
        "message": "Access token data is incorrect"
    })


@auth_reg_router.post('/forgot-password')
async def forgot_password(email: str = Form(...), db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.email == email))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{ "message": "Такого пользователя не существует" }])
    
    token = serializer.dumps(user.email, salt="reset_password")

    confirmation_url = f"{SERVER_ADDRES}/reset_password?token={token}"

    await send_reset_email(user.email, confirmation_url)

    return JSONResponse({
        "message": f"Ссылка на страницу для смены пароля отправлена на email"
    })
    

@auth_reg_router.post('/reset-password')
async def reset_password(token: str, form_data: ResetPasswordModel, db: AsyncSession = Depends(get_db)):
    try:
        email = serializer.loads(token, salt="reset-password", max_age=300)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ссылка истекла."
        )

    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{ "message": "Пользователь не найден" }]

        )
    
    if verify_password(form_data.new_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{ "message": "Новый пароль не должен совпадать со старым" }]
        )

    user.password = hash_password(form_data.new_password)

    try:
        await db.commit()
        return JSONResponse({
            "message": "Пароль успешно обновлен"
        })
    
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[{ "message": "Ошибка при обновлении пароля" }]
        )