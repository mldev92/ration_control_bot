from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from tgbot.dialogs.states import MainMenuState

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuState.start_menu, mode=StartMode.RESET_STACK)


# @user_router.startup
# async def menu_on_start(bot: Bot, dialog_manager: DialogManager):
#     await dialog_manager.start(MainMenuState.start_menu, mode=StartMode.RESET_STACK)
#     await bot.
