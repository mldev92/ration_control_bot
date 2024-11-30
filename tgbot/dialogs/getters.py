import json
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


@dataclass
class Product:
    product_id: int
    receipt_id: int
    name: str
    # quantity: int
    # weight: int
    # unit: str
    # calories: int
    # predicted_category: str
    created_at: str
    # store_name: str


async def get_receipts(dialog_manager: DialogManager, **kwargs):

    # x = json.dumps(dialog_manager.event.model_dump(), default=str)
    # print(x)

    repo = dialog_manager.middleware_data.get("repo")

    query_res = await repo.receipts.get_receipt_by_user_id(user_id=dialog_manager.event.from_user.id)
    print(f'{query_res=}')
    print(query_res[0].purchased_at)
    return {
        "receipts": query_res
    }
    # return {
    #     "receipts": [
    #         Receipt(1, 123456789, 'json_data', '16.11.2024', 'Пяткрочка'),
    #         Receipt(2, 123456789, 'json_data', '10.11.2024', 'Пяткрочка'),
    #         Receipt(3, 123456789, 'json_data', '03.11.2024', 'Пяткрочка'),
    #         Receipt(4, 123456789, 'json_data', '25.10.2024', 'Пяткрочка'),
    #         Receipt(5, 123456789, 'json_data', '20.10.2024', 'Пяткрочка'),
    #         Receipt(6, 123456789, 'json_data', '13.10.2024', 'Пяткрочка'),
    #         Receipt(7, 123456789, 'json_data', '05.10.2024', 'Пяткрочка'),
    #         Receipt(8, 123456789, 'json_data', '28.09.2024', 'Пяткрочка'),
    #         Receipt(9, 123456789, 'json_data', '22.09.2024', 'Пяткрочка'),
    #         Receipt(10, 123456789, 'json_data', '12.09.2024', 'Пяткрочка'),
    #         Receipt(11, 123456789, 'json_data', '08.09.2024', 'Пяткрочка'),
    #         Receipt(12, 123456789, 'json_data', '01.09.2024', 'Пяткрочка'),
    #     ]
    # }


async def get_products(dialog_manager: DialogManager, **kwargs):
    return {
        "products": [
            Product(1, 1, 'Напиток ДОБРЫЙ Малина, ПЭТ, 1 л', '16.11.2024'),
            Product(2, 1, 'Пакет майка ДА BIO большой', '10.11.2024'),
            Product(3, 1, 'Напиток ДОБРЫЙ Кола, ПЭТ, 1 л', '03.11.2024'),
            Product(4, 1, 'ИкрЛососСол95г', '25.10.2024'),
            Product(5, 1, 'Бананы кг', '20.10.2024'),
            Product(6, 1, 'ПивоКлассичЗолБочка0,45ж/б', '13.10.2024'),
            Product(7, 1, 'Напиток ДОБРЫЙ Малина, ПЭТ, 1 л', '05.10.2024'),
            Product(8, 1, 'Пакет майка ДА BIO большой', '28.09.2024'),
            Product(9, 1, 'Напиток ДОБРЫЙ Кола, ПЭТ, 1 л', '22.09.2024'),
        ]
    }
