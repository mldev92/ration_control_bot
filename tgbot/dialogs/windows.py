from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, Button, Row, Start, Back, SwitchTo, Cancel, Next, ScrollingGroup, Select, \
    Group, ListGroup
from aiogram_dialog.widgets.text import Multi, Const, Format, List
from aiogram.types import ContentType, Message

from tgbot.dialogs.getters import get_name, get_receipts, get_products
from tgbot.dialogs.selected import select_statistics, select_xml_or_json, selected_receipt
from tgbot.dialogs.states import MainMenuState, ReceiptInput, ReceiptsProducts, StatisticsState

d_start_menu = Dialog(
    Window(
        Format('👋 Приветствую, {name}'),
        Button(
            Const('🍽️ ИЗП: 60 📊'),
            id="d1w1_b_index",
        ),
        Button(
            Const('⚡ 35000 ккал. за период (1100/день)'),
            id="d1w1_b_kkal",
        ),
        Group(
            Button(
                Const("🔢 Статистика "),
                id="d1w1_b_statistics",
                on_click=select_statistics,
            ),
            Start(
                Const("📋 Чеки "),
                id="d2w3_b_receipts",
                state=ReceiptsProducts.receipts,
                mode=StartMode.RESET_STACK,
            ),
            Button(
                Const("🗓️ Период (30 дней)"),
                id="d1w1_b_period",
            ),
            Start(
                Const("➕ Добавить чек ✏️"),
                id="d1w1_b_add_check",
                state=ReceiptInput.input1,
                mode=StartMode.RESET_STACK
            ),
            width=2,
        ),
        state=MainMenuState.start_menu,
    ),
    getter=get_name,
    name='d_start_menu'
)

d_receipt_input = Dialog(
    Window(
        Const("Выберете как добавить чек:"),
        Group(
            Button(
                Const("👇 Добавить вручную"),
                id="d2w1_b_manually",
            ),
            Button(
                Const("🖼️ По фото"),
                id="d2w1_b_by_photo",
            ),
            Next(
                Const("📜 Добавить XML / JSON"),
            ),
            Start(
                Const("🏠 На главную"),
                id="d2w3_b_home",
                state=MainMenuState.start_menu,
                mode=StartMode.RESET_STACK,
            ),
            width=1,

        ),
        state=ReceiptInput.input1
    ),
    Window(
        Const("📜 Отправьте XML / JSON файл: "),
        MessageInput(select_xml_or_json, content_types=[ContentType.DOCUMENT]),
        state=ReceiptInput.input2,
    ),
    Window(
        Const("Далее:"),
        Group(
            SwitchTo(
                Const("🧾 Добавить еще чек ➕"),
                id="d2w3_b_back_to_input1",
                state=ReceiptInput.input1,
            ),
            Start(
                Const("📃 Чеки "),
                id="d2w3_b_receipts",
                state=ReceiptsProducts.receipts,
                mode=StartMode.RESET_STACK,
            ),
            width=2,
        ),
        Start(
            Const("🏠 На главную"),
            id="d2w3_b_home",
            state=MainMenuState.start_menu,
            mode=StartMode.RESET_STACK,
        ),
        state=ReceiptInput.input3
    ),
    name='d_receipt_input',
)

d_receipts = Dialog(
    Window(
        Const("📖 Чеки: "),
        ScrollingGroup(
            Select(
                id="receipt_select",
                items="receipts",
                item_id_getter=lambda item: item.receipt_id,
                text=Format("🧾 {item.purchased_at}"),
                on_click=selected_receipt,
            ),
            id="receipts_group",
            height=7,
            width=1,
            hide_on_single_page=True,
        ),
        Start(
            Const("🏠 На главную"),
            id="d3w1_b_home",
            state=MainMenuState.start_menu,
            mode=StartMode.RESET_STACK,
        ),
        state=ReceiptsProducts.receipts,
        getter=get_receipts,
    ),
    Window(
        Format("🧺 Продукты из чека №{products[0].receipt_id}: \n"),
        # Const("🧺 Продукты чек {item.receipt_id}: \n"),
        # ScrollingGroup(
        #     Select(
        #         id="products_select",
        #         items="products",
        #         item_id_getter=lambda item: item.product_id,
        #         text=Format("➡️ {item.name}"),
        #     ),
        #     id="products_group",
        #     height=7,
        #     width=1,
        #     hide_on_single_page=True,
        # ),
        List(
            Format(" 🔸 {item.name}\n--------------------------------------------------------------"),
            id="products_",
            items="products",
        ),
        Back(
            Const('Назад')
        ),
        Start(
            Const("🏠 На главную"),
            id="d3w2_b_home",
            state=MainMenuState.start_menu,
            mode=StartMode.RESET_STACK,
        ),
        state=ReceiptsProducts.concrete_receipt,
        getter=get_products,
    ),
)
