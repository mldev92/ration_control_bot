from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Column, Button, Row, Start
from aiogram_dialog.widgets.text import Multi, Const, Format

from tgbot.dialogs.getters import get_name
from tgbot.dialogs.selected import select_statistics
from tgbot.dialogs.states import MainMenuState, ReceiptInput, ReceiptsProducts, StatisticsState


d_start_menu = Dialog(
    Window(
        Format('Приветствую, {name}'),
        Button(
            Const('ИЗП: 60'),
            id="d1w1_b_index",
        ),
        Button(
            Const('35000 ккал. за период (1100/день)'),
            id="d1w1_b_kkal",
        ),
        Row(
            Button(
                Const("Статистика"),
                id="d1w1_b_statistics",
                on_click=select_statistics,
            ),
            Button(
                Const("Чеки"),
                id="d1w1_b_receipts",
            ),
        ),
        Button(
            Const("Период (30 дней)"),
            id="d1w1_b_period",
        ),
        Start(
            Const("Добавить чек"),
            id="d1w1_b_add_check",
            state=ReceiptInput.input1,
            mode=StartMode.RESET_STACK
        ),
        state=MainMenuState.start_menu,
    ),
    getter=get_name,
    name='d_start_menu'
)


d_receipt_input = Dialog(
    Window(
        Const("Выберете как добавить чек:"),
        Column(
            Button(
                Const("Добавить вручную"),
                id="d2w1_b_manually",
            ),
            Button(
                Const("По фото"),
                id="d2w1_b_by_photo",
            ),
            Button(
                Const("Добавить XML"),
                id="d2w1_b_by_xml",
            ),

        ),
        state=ReceiptInput.input1
    ),
    name='d_receipt_input',
)
