import json
from passlib.context import CryptContext
from smtplib import SMTPRecipientsRefused
from fastapi_mail import FastMail, MessageSchema
from fastapi import HTTPException
from config import email_config
import re

def load_services():
    with open("data/popular_services.json", "r", encoding="utf-8") as file:
        return json.load(file)


### Password encryption for writing to the database ###
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


### Validation of sending a message by email ###
async def send_registration_email(email: str, confirmation_url: str):
    message = MessageSchema(
        subject="Подтверждение регистрации",
        recipients=[email],
        body=f"Перейдите по ссылке для подтверждения: {confirmation_url}",
        subtype="plain",
    )
    fm = FastMail(email_config)

    try:
        await fm.send_message(message)
    except SMTPRecipientsRefused as e:
        invalid_recipients = list(e.recipients.keys())
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Некорректный адрес получателя.",
                "invalid_recipients": invalid_recipients,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки письма."
        )
    

def validation_translate(message: str, field: str):
    """Переводит сообщения валидации на русский язык."""
    
    email_invalid_characters_match = re.match( # Проверка сообщений с недопустимыми символами в email
        r"value is not a valid email address: The part after the @-sign contains invalid characters: (.+).",
        message,
    )
    if email_invalid_characters_match:
        invalid_characters = email_invalid_characters_match.group(1)
        return (
            f"Значение поля '{field}' не является действительным адресом электронной почты: "
            f"часть после знака @ содержит недопустимые символы: {invalid_characters}."
        )
    
    match message:
        case "String should have at least 4 characters":
            return f"Длина поля '{field}' должна быть не меньше 4 символов."
        
        case "String should have at least 8 characters":
            return f"Длина поля '{field}' должна быть не меньше 8 символов."
        
        case "String should have at most 50 characters":
            return f"Длина поля '{field}' должна быть не больше 50 символов."

        case "value is not a valid email address: An email address must have an @-sign.":
            return f"Поле '{field}' должно содержать символ '@'."

        case "value is not a valid email address: The part after the @-sign is not valid. It should have a period.":
            return f"Значение поля '{field}' не является действительным адресом электронной почты: часть после знака @ неверна."
        
        case "value is not a valid email address: An email address cannot have a period immediately after the @-sign.":
            return f"Значение поля '{field}' не является допустимым адресом электронной почты: адрес электронной почты не может иметь точку сразу после знака @."
        
        case "value is not a valid email address: An email address cannot end with a period.":
            return f"Значение поля '{field}' не является действительным адресом электронной почты: адрес электронной почты не может заканчиваться точкой."
        
        case "value is not a valid email address: There must be something after the @-sign.":
            return f"Значение поля '{field}' не является действительным адресом электронной почты: после знака @ должно быть что-то."
        
        case _:
            return message