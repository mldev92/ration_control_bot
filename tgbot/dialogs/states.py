from aiogram.fsm.state import State, StatesGroup


class MainMenuState(StatesGroup):
    start_menu = State()


class StatisticsState(StatesGroup):
    statistics = State()


class ReceiptInput(StatesGroup):
    input1 = State()
    input2 = State()


class ReceiptsProducts(StatesGroup):
    receipts = State()
    products = State()
