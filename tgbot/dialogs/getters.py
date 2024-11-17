from dataclasses import dataclass
from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def get_name(dialog_manager: DialogManager, **kwargs):
    return {
        'name': dialog_manager.event.from_user.first_name
    }


@dataclass
class Receipt:
    receipt_id: int
    user_id: int
    receipt_data: str
    created_at: str
    store_name: str


async def get_receipts(dialog_manager: DialogManager, **kwargs):
    return {
        "receipts": [
            Receipt(1, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(2, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(3, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(4, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(5, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(6, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(7, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(8, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(9, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(10, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(11, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
            Receipt(12, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
        ]
    }
