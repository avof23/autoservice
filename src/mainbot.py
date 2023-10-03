"""This module declares a telegram bot, connects its routers and basic handlers"""
import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.storage.memory import MemoryStorage

from constants import LANG, INTERVAL_PUSH_PLANNED, INTERVAL_PUSH_COMPLETE, template
from constants import NEW_STATUS_ID, READY_STATUS_ID
import pushed
import statuses
import register


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(statuses.router_status)
dp.include_router(register.router_register)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n{template[LANG]['welcome']}")


async def setup_bot_commands(bot) -> None:
    """
    Function generate menu for bot instance
    :param bot: class Bot link
    :return: None
    """
    bot_commands = [
        BotCommand(command="/help", description=template[LANG]['menu-help']),
        BotCommand(command="/register", description=template[LANG]['menu-register']),
        BotCommand(command="/cancel", description=template[LANG]['menu-cancel']),
        BotCommand(command="/status", description=template[LANG]['menu-status']),
        BotCommand(command="/info", description=template[LANG]['menu-info'])
    ]
    await bot.set_my_commands(bot_commands)


@dp.message(Command("help", ignore_case=True))
async def view_help(message: types.Message) -> None:
    """This handler will print help about all commands for this chatbot.
    receive /help command
    """
    await message.answer(template[LANG]['help'])


async def push_message(user_id: int, msg: str, bot: Bot) -> None:
    """
    Function send message to user chat
    :param user_id: int Telegram user ID who can receiving message
    :param msg: str Test message
    :param bot: class Bot link
    :return: None
    """
    await bot.send_message(user_id, msg)


async def control_push_message(timer: int, push_type: int, bot: Bot) -> None:
    """
    The function, after a specified period of time,
    receives a list of submissions from the database and initiates sending
    :param timer: int seconds sleep between send messages
    :param push_type: int message type identifier
    :param bot: class Bot link
    :return: None
    """
    pushed_list = []
    while True:
        await asyncio.sleep(timer)
        pushed_list.clear()
        for recipient in pushed.get_recipients_db(push_type):
            await push_message(recipient['client_id'], template[LANG][f'push-{push_type}'].format(**recipient), bot)
            pushed_list.append(recipient['id'])
        pushed.set_pushed_db(pushed_list)


async def main() -> None:
    """Initialize Bot instance with a default parse mode which will be passed to all API calls"""
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_bot_commands(bot)
    asyncio.create_task(control_push_message(INTERVAL_PUSH_PLANNED, NEW_STATUS_ID, bot))
    asyncio.create_task(control_push_message(INTERVAL_PUSH_COMPLETE, READY_STATUS_ID, bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
