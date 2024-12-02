import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from config import DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_connection_to_database():
    """Тест подключения к базе данных"""
    if not DATABASE_URL:
        raise AssertionError("DATABASE_URL не задан. Проверьте конфигурацию.")

    engine = create_async_engine(DATABASE_URL, echo=True)
    try:
        logger.info("Проверка подключения к базе данных...")
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            assert result.scalar() == 1, "Ошибка выполнения запроса SELECT 1"
            assert not connection.closed, "Соединение к базе данных не установлено"
        logger.info("Подключение к базе данных успешно")
    except OperationalError as e:
        raise AssertionError(f"Ошибка подключения к базе данных: {e}")
    except Exception as e:
        raise AssertionError(f"Неизвестная ошибка при работе с базой данных: {e}")
    finally:
        await engine.dispose()
        logger.info("Соединение с базой данных закрыто")