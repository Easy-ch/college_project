from pydantic import BaseModel, EmailStr, Field, model_validator
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi import status

class RegisterUser(BaseModel):
    email: EmailStr
    username: str = Field(...,
                            min_length=4,
                            max_length=50,
                            pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$'
                        )
    
    password: str = Field(
                        ...,
                        min_length=8,
                        max_length=50,
                        pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$'
                    )
    
    password_confirm: str = Field(
                                ...,
                                min_length=8,
                                max_length=50,
                                pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$'
                            )

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