import json

from bot.handlers.hander import Handler, HandlerStatus
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage


class SizeSelectionHander(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_SIZE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    def handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_small": "S (25cm)",
            "size_medium": "M (30cm)",
            "size_large": "L (35cm)",
            "size_xl": "XL (40cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        order_json["pizza_size"] = pizza_size

        storage.update_user_order_json(telegram_id, order_json)
        storage.update_user_state(telegram_id, "WAIT_FOR_DRINK")
        messenger.answerCallbackQuery(update["callback_query"]["id"])
        messenger.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        messenger.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Please select drink",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Coca-Cola", "callback_data": "drink_coca_cola"},
                            {"text": "Sprite", "callback_data": "drink_sprite"},
                        ],
                        [
                            {
                                "text": "Orange Juice",
                                "callback_data": "drink_orange_juice",
                            },
                            {
                                "text": "Apple Juice",
                                "callback_data": "drink_apple_juice",
                            },
                        ],
                        [
                            {"text": "Without Drink", "callback_data": "drink_none"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
