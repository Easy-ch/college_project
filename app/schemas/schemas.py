from pydantic import BaseModel, EmailStr, Field, model_validator,field_validator
from fastapi.exceptions import HTTPException
from fastapi import status
import re
from typing import Optional

class RegisterUser(BaseModel):
    email: EmailStr
    
    username: str = Field(...,
                          min_length=4,
                          max_length=50,
                          pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$')
    
    password: str = Field(...,
                          min_length=8,
                          max_length=50,
                          pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$')
    
    password_confirm: str = Field(...,
                                  min_length=8,
                                  max_length=50,
                                  pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$')

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "field": ["password",
                              "password_confirm"],
                    "message": "Пароли не совпадают"
                }
            )
        return self
    
    
class LoginUser(BaseModel):
    login: str = Field(...,
                       min_length=4,
                       max_length=50,
                       pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$',
                       description="Логин или Email")
    password: str = Field(...,
                          min_length=8,
                          max_length=30,
                          description="Пароль")



class ResetPasswordModel(BaseModel):
    new_password: str = Field(...,
                              min_length=8,
                              max_length=30,
                              description="Пароль")
    

class ProfileModel(BaseModel):
    username_change: Optional[str] = Field(default=None,max_length=50)
    phone_number:Optional[str] = Field(None,description="Номер телефона в формате +7XXXXXXXXXX")
    password: Optional[str] = Field(None,max_length=30)
    new_password: Optional[str] = Field(None,max_length=30)

    @field_validator("username_change")
    def validate_username_change(cls,value):
        if not value:
            return value
        if  len(value)<4:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "field": ["username_change"],
                    "message": "Имя должно содержать минимум 4 символа"
                }
            )
        pattern = r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$'  
        if not re.match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "field": ["username_change"],
                    "message": "Имя может содержать только буквы, цифры, и символы ._-"
                }
            )
        return value

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if value:
            pattern = r'^\+7\d{10}$'
            if not re.match(pattern, str(value)):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "field": ["phone_number"],
                        "message": "Введите номер телефона в формате +7XXXXXXXXXX"
                    }
                )
        return value
