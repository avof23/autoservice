"""This module creates a router that processes register requests from users"""
import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

# from db import Orders, Clients
from constants import LANG, template, VALUT, NEW_STATUS_ID
import keyboards as kb


class OrderWork(StatesGroup):
    """Class specified States from FSM"""
    choosing_work_name = State()
    choosing_work_date = State()
    choosing_work_time = State()


router_register = Router()


@router_register.message(Command("cancel"))
@router_register.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Allow user to cancel registration action"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Cancelled.")


@router_register.message(Command("register"))
async def process_reg_command(message: Message, state: FSMContext) -> None:
    """
        This handler receives messages with `/register` command
        and output InlineKeyboard
    """
    await state.set_state(OrderWork.choosing_work_name)
    await state.update_data(client_id=message.from_user.id, client_name=message.from_user.full_name,
                            description=f"Register From TB {datetime.date}")
    await message.answer(template[LANG]['workchoice'], reply_markup=kb.works_keyboard_fab())


@router_register.callback_query(OrderWork.choosing_work_name, kb.WorksCallbackFactory.filter())
async def callbacks_works_select_fab(
        callback: CallbackQuery,
        callback_data: kb.WorksCallbackFactory, state: FSMContext):
    """
        Function receives callback and save value in FSM context MemoryStorage
        Sends a response to the user of his choice
    """
    await state.update_data(status_id=NEW_STATUS_ID, order_summ=callback_data.price,
                            credit_summ=callback_data.price * (-1), work_id=callback_data.id)
    await callback.message.edit_text(f"{template[LANG]['workselect']}: {callback_data.work_name}, "
                                     f"{template[LANG]['pricetext']}: {callback_data.price} {VALUT}\n")
    await callback.answer()
    await state.set_state(OrderWork.choosing_work_date)
    await callback.message.answer(text=template[LANG]['datechoice'], reply_markup=kb.date_keyboard_fab())


@router_register.message(OrderWork.choosing_work_name)
async def callback_works_select_incorrectly(message: Message):
    """Function for reselecting a value in case of incorrect input from the client"""
    await message.answer(f"Incorrect select\n\n{template[LANG]['workchoice']}",
                             reply_markup=kb.works_keyboard_fab())


@router_register.callback_query(OrderWork.choosing_work_date, F.data.regexp(r"\d{2}\.\d{2}"))
async def callbacks_days_select_fab(callback: CallbackQuery, state: FSMContext):
    """
        Function receives callback and save value in FSM context MemoryStorage
        Sends a response to the user of his choice
    """
    await state.update_data(start_date='', end_date='')
    await callback.message.edit_text(f"{template[LANG]['dateselect']}: {callback.data}")
    await callback.answer()
    await state.set_state(OrderWork.choosing_work_time)
    await callback.message.answer(text=template[LANG]['timechoice'], reply_markup=kb.time_keyboard_fab())


@router_register.message(OrderWork.choosing_work_date)
async def callbacks_days_select_incorrectly(message: Message):
    """Function for reselecting a value in case of incorrect input from the client"""
    await message.answer(f"Incorrect select\n\n{template[LANG]['datechoice']}",
                         reply_markup=kb.date_keyboard_fab())


@router_register.callback_query(OrderWork.choosing_work_time, F.data.regexp(r"\d{2}:\d{2}"))
async def callbacks_time_select_fab(callback: CallbackQuery, state: FSMContext):
    """
        Function receives callback and save value in FSM context MemoryStorage
        Sends a response to the user of his choice
    """
    await state.update_data(start_date='', end_date='')
    user_data = await state.get_data()
    await callback.message.edit_text(f"{template[LANG]['timeselect']}: {callback.data}")
    await callback.answer()
    await state.clear()


@router_register.message(OrderWork.choosing_work_time)
async def callbacks_time_select_incorrectly(message: Message):
    """Function for reselecting a value in case of incorrect input from the client"""
    await message.answer(f"Incorrect select\n\n{template[LANG]['timechoice']}",
                         reply_markup=kb.time_keyboard_fab())


if __name__ == '__main__':
    pass
