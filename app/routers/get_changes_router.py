from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Request,Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from models.models import User
from config import REFRESH_TOKEN_EXPIRE_DAYS
from config import *
from jwt_utils import create_access_token,create_refresh_token
from schemas.schemas import ProfileModel
from routers.auth_reg_router import get_current_user
from utils import hash_password,verify_password

get_changes_router = APIRouter()


@get_changes_router.put('/upload_change_profile')
async def upload_form(form: ProfileModel, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.username == user['sub']) | (User.email == user['sub']))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if form.username_change:
        if  form.username_change != user.username:
            username_query = select(User).where(User.username == form.username_change)
            username_result = await db.execute(username_query)
            existing_user = username_result.scalar_one_or_none()
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail={ "message": "Пользователь с таким username уже существует" })
            user.username = form.username_change
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail={ "message": "Новый username не должен совпадать со старым" })
    
    if form.phone_number:
        if form.phone_number != user.phone_number:
            phone_number_query = select(User).where(User.phone_number == form.phone_number)
            phone_number_result = await db.execute(phone_number_query)
            existing_number = phone_number_result.scalar_one_or_none()
            if existing_number:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail={ "message": "Пользователь с таким номером телефона уже существует" })
            user.phone_number = form.phone_number
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={ "message": "Новый телефон не должен совпадать со старым" })
    
    if form.password and form.new_password:
        if not verify_password(form.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Текущий пароль неверен"}
            )

        if form.new_password == form.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Новый пароль не должен совпадать с текущим"}
            )

        user.password = hash_password(form.new_password)



    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    try:
        await db.commit()
        response = JSONResponse({"message": "Данные успешно обновлены","username":user.username,"phone_number": user.phone_number,"access_token":access_token})
        print(response)
        response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,   # Используйте True для HTTPS
        samesite="Strict",
        expires=(datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    )
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка при обновлении данных")
    
    return response


