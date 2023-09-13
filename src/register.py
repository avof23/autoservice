"""This module creates a router that processes register requests from users"""
import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from db import Orders, Clients
from constants import LANG, VALUT, NEW_STATUS_ID
from text_templates import template
import keyboards as kb


router_register = Router()
pre_order = Orders()
pre_client = Clients()


@router_register.message(Command("register"))
async def process_reg_command(message: Message):
    """
        This handler receives messages with `/register` command
        and output InlineKeyboard
    """
    global pre_client

    pre_client.id = message.from_user.id
    pre_client.name = message.from_user.full_name
    pre_client.description = f"Register From TB {datetime.date}"
    await message.answer(template[LANG]['workchoice'], reply_markup=kb.works_keyboard_fab())


@router_register.callback_query(kb.WorksCallbackFactory.filter())
async def callbacks_works_select_fab(
        callback: CallbackQuery,
        callback_data: kb.WorksCallbackFactory):
    """
        Function receives callback and save value
        Sends a response to the user of his choice
    """
    global pre_order, pre_client

    pre_order.status_id = NEW_STATUS_ID
    pre_order.order_summ = callback_data.price
    pre_order.credit_summ = callback_data.price * (-1)
    pre_order.client_id = pre_client.id
    await callback.message.edit_text(f"{template[LANG]['workselect']}: {callback_data.work_name}, "
                                     f"{template[LANG]['pricetext']}: {callback_data.price} {VALUT}\n")
    await callback.answer()
    await callback.message.answer(text=template[LANG]['datechoice'], reply_markup=kb.date_keyboard_fab())


@router_register.callback_query(F.data.regexp(r"\d{2}\.\d{2}"))
async def callbacks_days_select_fab(callback: CallbackQuery):
    """
        Function receives callback and save value
        Sends a response to the user of his choice
    """
    global pre_order

    # pre_order.start_date = ''
    # pre_order.end_date = ''
    await callback.message.edit_text(f"{template[LANG]['dateselect']}: {callback.data}")
    await callback.answer()
    await callback.message.answer(text=template[LANG]['timechoice'], reply_markup=kb.time_keyboard_fab())


@router_register.callback_query(F.data.regexp(r"\d{2}:\d{2}"))
async def callbacks_time_select_fab(callback: CallbackQuery):
    """
        Function receives callback and save value
        Sends a response to the user of his choice
    """
    global pre_order

    # pre_order.start_date = ''
    # pre_order.end_date = ''
    await callback.message.edit_text(f"{template[LANG]['timeselect']}: {callback.data}")
    await callback.answer()


if __name__ == '__main__':
    pass
