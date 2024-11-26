from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db import get_db
from models.models import User
from utils import hash_password
from schemas.schemas import RegisterUser
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy import select
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from config import *
import logging

# email_config = ConnectionConfig (**EmailConfig().model_dump())
# email_config = ConnectionConfig(
#     **EmailConfig(MAIL_STARTTLS=True).model_dump()
# )
email_config = ConnectionConfig(
    MAIL_USERNAME="08042007artem@mail.ru",
    MAIL_PASSWORD="CFk2uEyeCb5d3DuUpVke",
    MAIL_FROM="08042007artem@mail.ru",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.mail.ru",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)


serializer = URLSafeTimedSerializer(SECRET_KEY)

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
        # return {"message": "Регистрация успешна"}
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











# @app2.post('/login')
# async def validation(form:Annotated[Form()],user:User ):
#     if form.login != await get_user(user['email']):
#         raise HTTPException(404,"Not_found_user")
#     if form.password != await get_user(user['password']):
#         raise HTTPException(404,'Invalid_password')
#     return {"status":"success"}