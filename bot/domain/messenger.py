from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    async def get_updates(**params) -> dict: ...

    @abstractmethod
    async def send_message(chat_id: int, text: str, **params) -> dict: ...

    @abstractmethod
    async def delete_message(chat_id: int, message_id: int) -> dict: ...

    @abstractmethod
    async def answer_callback_query(callback_query_id: str, **params) -> dict: ...
