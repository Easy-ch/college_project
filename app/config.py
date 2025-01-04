from fastapi_mail import ConnectionConfig
from itsdangerous import URLSafeTimedSerializer

START_WITH_TEST = False
DATABASE_URL    = "postgresql+asyncpg://server_root:xDdmZeUxFYrlE83zbyBT7XH-hBSpNN07k6UjQicOejA@127.0.0.1:5432/project"
SECRET_KEY      = ""
# SERVER_ADDRES   = "http://188.242.78.13/auth"
SERVER_ADDRES = "http://0.0.0.0:8000/auth"
# SERVER_ADDRES = "http://127.0.0.1:8000/auth"
IS_DEBUG        = True
serializer      = URLSafeTimedSerializer(SECRET_KEY)

email_config = ConnectionConfig(
    MAIL_USERNAME="vanuxatelny@gmail.com",
    MAIL_PASSWORD="aown jefb dxgx zzvb",
    MAIL_FROM="vanuxatelny@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)

# SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7