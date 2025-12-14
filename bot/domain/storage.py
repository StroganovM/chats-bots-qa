from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    async def recreate_database() -> None: ...

    @abstractmethod
    async def persist_update(updates: list) -> None: ...

    @abstractmethod
    async def ensure_user_exists(telegram_id: int) -> None: ...

    @abstractmethod
    async def clear_user_order_and_state(telegram_id: int) -> None: ...

    @abstractmethod
    async def update_user_state(telegram_id: int, state: str) -> None: ...

    @abstractmethod
    async def get_user(telegram_id: int) -> dict: ...

    @abstractmethod
    async def update_user_order_json(telegram_id: int, order: dict) -> None: ...
