from config import SECRET_KEY
import sys
import uvicorn
import logging
import pytest
from fastapi import FastAPI, Request
from routers.pages_router import router as router_pages
from routers.auth_reg_router import auth_reg_router as router_validate
from routers.get_changes_router import get_changes_router as router_changes
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import START_WITH_TEST
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from db import init_db
from pathlib import Path
from secrets import token_urlsafe
from utils import validation_translate


green = "\033[32m"
reset = "\033[0m"


if START_WITH_TEST:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

if START_WITH_TEST:
    logging.info("Приложение запущено в тестовом режиме\n")
    
    exit_code = pytest.main(['./tests/data_base_connect.py', "tests"])
    if exit_code != 0:
        logging.error("Тесты завершились с ошибками. Код выхода: %d", exit_code)
        sys.exit(exit_code)
    else:
        logging.info(f"{green}Тесты пройдены успешно{reset}\n")



@asynccontextmanager
async def lifespan(app: FastAPI):
        await init_db()
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_pages)
app.include_router(router_validate, prefix="/auth")
app.include_router(router_changes,prefix='/changes')
app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'))
origins = [
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик ошибок валидации Pydantic с переводом на русский язык."""
    errors = []
    for err in exc.errors():
        field_path = ".".join(map(str, err.get("loc", [])))

        if field_path.startswith("body."):
            field_path = field_path[5:]

        errors.append({"field": field_path, "message": validation_translate(err.get("msg", "Ошибка"), field_path)})

    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )

@app.exception_handler(404)
async def get_404_error(request:Request, exc:404):
    return FileResponse("templates/error404.html",
                        status_code=404)


if not START_WITH_TEST:
    if __name__ == '__main__':
        if SECRET_KEY:
            key_file = Path("secret.key")
            if not key_file.exists():
                key = token_urlsafe(32)
                key_file.write_text(key)
                SECRET_KEY = key
            else:
                SECRET_KEY = key_file.read_text()

        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)