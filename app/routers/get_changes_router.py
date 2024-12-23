from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Request,Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models.models import User
from config import *
from schemas.schemas import ProfileModel
from routers.auth_reg_router import get_current_user

get_changes_router = APIRouter()


@get_changes_router.put('/upload_phone_field')
async def upload_field(form: ProfileModel, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(User).where((User.username == user['sub']) | (User.email == user['sub']))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    user.phone_number = form.phone_number
    try:
        await db.commit()
        return {"message": "Телефон успешно обновлён"}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка при обновлении телефона")


