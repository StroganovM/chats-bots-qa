from bot.handlers.hander import Handler
from bot.handlers.database_logger import DB_Logger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.message_start import MessageStart
from bot.handlers.pizza_selection import PizzaSelectionHander
from bot.handlers.pizza_size import SizeSelectionHander
from bot.handlers.pizza_drink import DrinkSelectionHander
from bot.handlers.pizza_order import ApproveOrderHander


def get_handlers() -> list[Handler]:
    return [
        DB_Logger(),
        EnsureUserExists(),
        MessageStart(),
        PizzaSelectionHander(),
        SizeSelectionHander(),
        DrinkSelectionHander(),
        ApproveOrderHander(),
    ]
