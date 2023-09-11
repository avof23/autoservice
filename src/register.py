"""This module creates a router that processes register requests from users"""
from sqlalchemy.orm import Session
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject

from db import engine, Orders
from constants import LANG, VALUT
from text_templates import template
import keyboards as kb


router_register = Router()


@router_register.message(Command("register"))
async def process_reg_command(message: Message):
    """
        This handler receives messages with `/register` command
        and output InlineKeyboard
    """
    await message.answer(template[LANG]['workchoice'], reply_markup=kb.works_keyboard_fab())


@router_register.callback_query(kb.WorksCallbackFactory.filter())
async def callbacks_works_select_fab(
        callback: CallbackQuery,
        callback_data: kb.WorksCallbackFactory):
    """
        Function receives callback and save value
        Sends a response to the user of his choice
    """
    await callback.message.edit_text(f"{template[LANG]['workselect']}: {callback_data.work_name}, "
                                     f"{template[LANG]['pricetext']}: {callback_data.price}{VALUT}")
    await callback.answer()

if __name__ == '__main__':
    pass
