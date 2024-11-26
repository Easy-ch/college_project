from pydantic import BaseModel, EmailStr, Field, model_validator
from fastapi.exceptions import RequestValidationError

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
            raise RequestValidationError("Пароли не совпадают.")
        return self
    

# class EmailConfig(BaseModel):
#     MAIL_USERNAME: str = "08042007artem@mail.ru"
#     MAIL_STARTTLS: bool = False
#     MAIL_PASSWORD: str = "CFk2uEyeCb5d3DuUpVke"
#     MAIL_FROM: str = "08042007artem@mail.ru"
#     MAIL_PORT: int = 465
#     MAIL_SERVER: str = "smtp.mail.ru"
#     MAIL_SSL_TLS: bool = True
#     MAIL_TLS: bool = False
#     MAIL_SSL: bool = True
#     USE_CREDENTIALS: bool = True

# class EmailConfig(BaseModel):
#     MAIL_USERNAME: str = "08042007artem@mail.ru"
#     MAIL_PASSWORD: str = "CFk2uEyeCb5d3DuUpVke"
#     MAIL_FROM: str = "08042007artem@mail.ru"
#     MAIL_PORT: int = 465
#     MAIL_SERVER: str = "smtp.mail.ru"
#     MAIL_STARTTLS: bool = False  # Use True for explicit TLS
#     MAIL_SSL_TLS: bool = True   # Use True for implicit TLS (port 465)
#     USE_CREDENTIALS: bool = True





# from fastapi import FastAPI, HTTPException, Depends
# from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import BaseModel, EmailStr

# # Инициализация FastAPI
# app = FastAPI()

# # Конфигурация для отправки email
# class EmailConfig(BaseModel):
#     MAIL_USERNAME: str = "your_email@example.com"
#     MAIL_PASSWORD: str = "your_password"
#     MAIL_FROM: str = "your_email@example.com"
#     MAIL_PORT: int = 587
#     MAIL_SERVER: str = "smtp.example.com"
#     MAIL_TLS: bool = True
#     MAIL_SSL: bool = False

# email_config = ConnectionConfig (
#                                     MAIL_USERNAME = EmailConfig.MAIL_USERNAME,
#                                     MAIL_PASSWORD = EmailConfig.MAIL_PASSWORD,
#                                     MAIL_FROM     = EmailConfig.MAIL_FROM,
#                                     MAIL_PORT     = EmailConfig.MAIL_PORT,
#                                     MAIL_SERVER   = EmailConfig.MAIL_SERVER,
#                                     MAIL_SSL_TLS  = EmailConfig.MAIL_TLS
#                                 )

# # Инициализация сериализатора токенов
# SECRET_KEY = "your_secret_key"  # Замените на безопасный ключ
# serializer = URLSafeTimedSerializer(SECRET_KEY)


# @app.post("/send-confirmation-email/")
# async def send_confirmation_email(email: EmailStr):
#     # Генерация токена
#     token = serializer.dumps(email, salt="email-confirmation")

#     # Ссылка для подтверждения
#     confirmation_url = f"http://localhost:8000/confirm-email/{token}"

#     # Отправка email
#     message = MessageSchema(
#         subject="Подтверждение регистрации",
#         recipients=[email],
#         body=f"Перейдите по ссылке для подтверждения: {confirmation_url}",
#         subtype="plain",
#     )

#     fm = FastMail(email_config)
#     await fm.send_message(message)

#     return {"message": "Письмо с подтверждением отправлено"}


# @app.get("/confirm-email/{token}")
# async def confirm_email(token: str):
#     try:
#         email = serializer.loads(token, salt="email-confirmation", max_age=300)  # 5 минут
#         return {"message": f"Email {email} успешно подтвержден!"}

#     except SignatureExpired:
#         raise HTTPException(
#             status_code=400,
#             detail="Срок действия ссылки истек. Пожалуйста, запросите новую."
#         )
#     except BadSignature:
#         raise HTTPException(
#             status_code=400,
#             detail="Недействительная ссылка подтверждения."
#         )






# class LoginUser(BaseModel):
#     login: str = Field(...,
#                        min_length=4,
#                        max_length=50,
#                        pattern=r'^[a-zA-Z0-9_.-а-яА-ЯёЁ]+$',
#                        description="Логин или Email")
#     password: str = Field(...,
#                           min_length=8,
#                           max_length=30,
#                           description="Пароль")