import pytest

from bot.dispatcher import Dispatcher
from bot.handlers.database_logger import DB_Logger

from tests.mock import Mock


@pytest.mark.asyncio
async def test_database_logger_handler():
    test_update = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 12345,
                "is_bot": False,
                "first_name": "DBTest",
                "username": "dbtestuser",
            },
            "chat": {
                "id": 12345,
                "first_name": "DBTest",
                "username": "dbtestuser",
                "type": "private",
            },
            "date": 1640995200,
            "text": "Hi, this is a db test message",
        },
    }

    persist_update_called = False

    async def persist_update(update: dict) -> None:
        nonlocal persist_update_called
        persist_update_called = True
        assert update == test_update

    async def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        return None

    mock_storage = Mock(
        {
            "persist_update": persist_update,
            "get_user": get_user,
        }
    )
    mock_messenger = Mock({})

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    db_logger = DB_Logger()
    dispatcher.add_handlers(db_logger)
    await dispatcher.dispatch(test_update)

    assert persist_update_called
