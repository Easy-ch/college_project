from fastapi_mail import ConnectionConfig
from itsdangerous import URLSafeTimedSerializer

START_WITH_TEST = False
DATABASE_URL    = "postgresql+asyncpg://server_root:qwertyuiop1@188.242.78.13:5432/project"
SECRET_KEY = ""
SERVER_ADDRES = "http://188.242.78.13"
IS_DEBUG = True

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