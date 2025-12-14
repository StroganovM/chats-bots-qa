import asyncio
from bot.handlers.handler import Handler, HandlerStatus
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage


class ApproveOrderHander(Handler):
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

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("order_")

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

        await asyncio.gather(
            storage.update_user_state(telegram_id, "ORDER_FINISHED"),
            messenger.answer_callback_query(update["callback_query"]["id"]),
            messenger.delete_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                message_id=update["callback_query"]["message"]["message_id"],
            ),
        )

        if callback_data == "order_approve":
            pizza_name = order_json.get("pizza_name", "Unknown")
            pizza_size = order_json.get("pizza_size", "Unknown")
            drink = order_json.get("pizza_drink", "Unknown")

            order_summary = f"""🍕 **Your Order Summary:**
            **Pizza:** {pizza_name}
            **Size:** {pizza_size}
            **Drink:** {drink}

            Thank you for your order!
            Send /start to new order."""

            await asyncio.gather(
                messenger.send_message(
                    chat_id=update["callback_query"]["message"]["chat"]["id"],
                    text=order_summary,
                    parse_mode="Markdown",
                ),
            )
        elif callback_data == "order_revoke":
            storage.clear_user_order_and_state(telegram_id)
            order_summary = """
            **Your order was revoked!**
            **Send /start to new order.**"""

            await asyncio.gather(
                messenger.send_message(
                    chat_id=update["callback_query"]["message"]["chat"]["id"],
                    text=order_summary,
                    parse_mode="Markdown",
                ),
            )

        return HandlerStatus.STOP
