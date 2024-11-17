from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from tgbot.dialogs.states import MainMenuState

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuState.start_menu, mode=StartMode.RESET_STACK)
