import asyncio
import json

from bot.handlers.handler import Handler, HandlerStatus
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

    async def handle(
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

        await asyncio.gather(
            storage.update_user_order_json(telegram_id, order_json),
            storage.update_user_state(telegram_id, "WAIT_FOR_DRINK"),
            messenger.answer_callback_query(update["callback_query"]["id"]),
        )

        await asyncio.gather(
            messenger.delete_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                message_id=update["callback_query"]["message"]["message_id"],
            ),
            messenger.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="Please select drink",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "Coca-Cola",
                                    "callback_data": "drink_coca_cola",
                                },
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
                                {
                                    "text": "Without Drink",
                                    "callback_data": "drink_none",
                                },
                            ],
                        ],
                    },
                ),
            ),
        )
        return HandlerStatus.STOP
