from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select

from xml.etree import ElementTree as ET
import json
from datetime import datetime

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.states import ReceiptInput, ReceiptsProducts


async def select_statistics(callback: CallbackQuery, button: Button, manager: DialogManager):
    return  # TODO:


async def select_xml_or_json(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    if not message.document:
        await message.answer("Please send a document containing the receipt.")
        return

    # x = json.dumps(dialog_manager.event.model_dump(), default=str)
    # print(x)

        # Get the file ID and file name
    file_id = message.document.file_id
    file_name = message.document.file_name.lower()

    def format_shopping_list(shopping_list_string):
        """Форматирует список покупок, добавляя нумерацию.

        Args:
          shopping_list_string: Строка, представляющая список покупок.

        Returns:
          Отформатированная строка с нумерованными элементами списка.
        """

        itms = shopping_list_string.split(';')
        formatted_list = []
        for i, itm in enumerate(itms, start=1):
            formatted_list.append(f"{i}. {itm.strip()}")
        return '\n\n'.join(formatted_list)

    async def handle_xml(receipt_data: bytes, message: Message):
        try:
            root = ET.fromstring(receipt_data)

            # Extract the receipt date
            receipt_Date_element = root.find(".//dateTime")
            receipt_Date = receipt_Date_element.text if receipt_Date_element is not None else "Unknown"
            receipt_Date = datetime.fromisoformat(receipt_Date).strftime("%Y-%m-%d - %H:%M")

            # Extract purchase item names
            purchase_names = []
            items = root.findall(".//items")
            for item in items:
                name_element = item.find("name")
                purchase_name = name_element.text if name_element is not None else "Unnamed Item"
                purchase_names.append(purchase_name)

            purchase_list = "; ".join(purchase_names)
            await message.answer(
                f"✅ Чек успешно загружен!\n\n📅 Дата покупок: \n\n{receipt_Date}\n\n🧾 Покупки: \n\n{format_shopping_list(purchase_list)}"
                f"\n\n         🏁      🏁      🏁"
            )

        except Exception as e:
            await message.answer(f"Error parsing XML receipt: {e}")

    async def handle_json(receipt_data: bytes, message: Message):
        try:
            # Parse JSON data
            receipts = json.loads(receipt_data.decode("utf-8"))

            # print(type(receipts), '::', receipts)
            # if not isinstance(receipts, list) or len(receipts) == 0:
            #     await message.answer("Invalid JSON format. Expected a non-empty list.")
            #     return

            if isinstance(receipts, list):
                # Use the first receipt in the list
                receipt = receipts[0]
            elif isinstance(receipts, dict):
                receipt = receipts
            else:
                await message.answer("Invalid JSON format.")
                return

            # Extract the receipt date
            receipt_Date = (
                receipt.get("ticket", {})
                .get("document", {})
                .get("receipt", {})
                .get("dateTime", "Unknown")
            )
            date_time_obj = datetime.fromisoformat(receipt_Date)
            receipt_Date = datetime.fromisoformat(receipt_Date).strftime("%Y-%m-%d - %H:%M")

            # Extract purchase item names (iterate through the list in 'items')
            items = (
                receipt.get("ticket", {})
                .get("document", {})
                .get("receipt", {})
                .get("items", [])
            )

            retailPlace = (
                receipt.get("ticket", {})
                .get("document", {})
                .get("receipt", {})
                .get("retailPlace", "")
            )

            if isinstance(items, list):  # Ensure items is a list
                purchase_names = [f"<i>{item.get('name', 'Unnamed Item')}</i> -<b>{item.get('quantity', 1)}шт.</b>" for
                                  item in items]
            else:
                purchase_names = ["Invalid items format"]
            purchase_list = "; ".join(purchase_names)

            # TODO: Add category prediction and extracted weight, unit and calories

            repo = dialog_manager.middleware_data.get("repo")

            # Create a new receipt or updates the existing one if a conflict occurs. It checks for conflict
            # based on the user_id and purchased_at.
            db_reciept = await repo.receipts.get_or_create_receipt(user_id=message.chat.id,
                                                      store_name=retailPlace,
                                                      receipt_data=items,
                                                      purchased_at=date_time_obj
                                                      )
            # print(f'{db_reciept=}')
            receipt_id = db_reciept.receipt_id

            for item in items:
                await repo.products.get_or_create_product(
                                                          receipt_id=receipt_id,
                                                          product_name=item.get('name', 'Unnamed Item'),
                                                          quantity=item.get('quantity', 1),
                                                         )


            await message.answer(
                f"✅ Чек успешно загружен!\n\nИз {retailPlace}\n\n📅 Дата покупок: \n\n{receipt_Date}\n\n🧾 "
                f"Покупки:\n\n{format_shopping_list(purchase_list)}"
                f"\n\n         🏁      🏁      🏁"
            )

        except Exception as e:
            await message.answer(f"Error parsing JSON receipt: {e}")

    try:
        # Use the bot instance to get the file URL
        bot = message.bot
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

        # Download the file content
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                receipt_data = await response.read()
                dialog_manager.dialog_data["receipt"] = receipt_data
                print(type(receipt_data), ':', receipt_data)
    except Exception as e:
        await message.answer(f"Error downloading document: {e}")
        return

    # Determine file type and parse
    try:
        if file_name.endswith(".xml"):
            await handle_xml(receipt_data, message)
        elif file_name.endswith(".json"):
            await handle_json(receipt_data, message)
        else:
            await message.answer("Unsupported file format. Please send an XML or JSON file.")
    except Exception as e:
        await message.answer(f"Error processing receipt: {e}")

    await dialog_manager.switch_to(ReceiptInput.input3)


async def selected_receipt(
        callback_query: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str,
):
    dialog_manager.dialog_data["receipt_id"] = item_id
    await dialog_manager.switch_to(ReceiptsProducts.concrete_receipt)
