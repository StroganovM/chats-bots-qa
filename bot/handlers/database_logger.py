from bot.handlers.hander import Handler, HandlerStatus
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage


class DB_Logger(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return True

    def handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        storage.persist_update(update)
        return HandlerStatus.CONTINUE
