"""This module declares a telegram bot, connects its routers and basic hadlers"""
import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from constants import LANG
from text_templates import template
import statuses
import register

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
dp.include_router(statuses.router_status)
dp.include_router(register.router_register)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n{template[LANG]['welcome']}")


@dp.message(Command("help", ignore_case=True))
async def view_help(message: types.Message) -> None:
    """This handler will print help about all commands for this chatbot.
    receive /help command
    """
    await message.answer(template[LANG]['help'])


@dp.message(Command("cancel", ignore_case=True))
async def view_help(message: types.Message) -> None:
    """This handler will cancel register process."""
    await message.answer(template[LANG]['cancel'])


async def main() -> None:
    """Initialize Bot instance with a default parse mode which will be passed to all API calls"""
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
