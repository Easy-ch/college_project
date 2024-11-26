import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from config import DATABASE_URL

@pytest.mark.asyncio
async def test_connection_to_database():
    """Тест подключения к базе данных по URL"""
    engine = create_async_engine(DATABASE_URL, echo=True)
    try:
        # Проверка соединения с базой данных
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            assert result.scalar() == 1, "Ошибка выполнения запроса"
            assert connection.closed is False, "Подключение к базе данных не установлено"
    except OperationalError as e:
        raise AssertionError(f"Ошибка подключения к базе данных: {e}")
    except Exception as e:
        raise AssertionError(f"Неизвестная ошибка: {e}")
    finally:
        # Закрытие соединения
        await engine.dispose()
