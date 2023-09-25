"""This module creates a router that processes register requests from users"""
import datetime

from sqlalchemy.orm import Session
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from db import engine, Orders, Clients, ContentOrders
from constants import LANG, template, VALUT, NEW_STATUS_ID
import keyboards as kb


class OrderWork(StatesGroup):
    """Class specified States from FSM"""
    choosing_work_name = State()
    choosing_work_date = State()
    choosing_work_time = State()


router_register = Router()


def update_client_db(id: int, name: str, descr: str) -> None:
    client = Clients()
    client.id = id
    client.name = name
    client.description = descr
    with Session(engine) as session:
        session.merge(client)
        session.commit()


def create_order_db(**kwargs) -> int:
    order = Orders()
    cont_order = ContentOrders()
    order.status_id = kwargs['status_id']
    order.client_id = kwargs['client_id']
    order.order_summ = kwargs['order_summ']
    order.credit_summ = kwargs['credit_summ']

    start_date = datetime.datetime.strptime(f"{kwargs['start_date']} {kwargs['start_time']}", '%d.%m.%Y %H:%M')
    end_date = start_date + datetime.timedelta(minutes=kwargs['norm_min'])
    order.start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d %H:%M')
    order.end_date = datetime.datetime.strftime(end_date, '%Y-%m-%d %H:%M')

    order.master_id = 1  # Master selection variable
    order.description = 'Order created in TB'
    cont_order.work_id = kwargs['work_id']
    cont_order.quantity = 1
    with Session(engine) as session:
        session.add(order)
        session.flush()
        session.refresh(order)

        cont_order.order_id = order.id
        session.add(cont_order)
        session.commit()
        return order.id


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
                            description=f"Register From TB {datetime.datetime.now().strftime('%d.%m.%Y')}")
    await message.answer(template[LANG]['workchoice'], reply_markup=kb.works_keyboard_fab())


@router_register.callback_query(OrderWork.choosing_work_name, kb.WorksCallbackFactory.filter())
async def callbacks_works_select_fab(
        callback: CallbackQuery,
        callback_data: kb.WorksCallbackFactory, state: FSMContext):
    """
        Function receives callback and save value in FSM context MemoryStorage
        Sends a response to the user of his choice
    """
    await state.update_data(status_id=NEW_STATUS_ID,
                            order_summ=callback_data.price, credit_summ=callback_data.price * (-1),
                            work_id=callback_data.id, norm_min=callback_data.norm_min,
                            work_type=callback_data.requirements)
    await callback.message.edit_text(f"{template[LANG]['workselect']}: {callback_data.work_name}, "
                                     f"{template[LANG]['pricetext']}: {callback_data.price} {VALUT}\n")
    await callback.answer()
    await state.set_state(OrderWork.choosing_work_date)
    await callback.message.answer(text=template[LANG]['datechoice'],
                                  reply_markup=kb.date_keyboard_fab(callback_data.requirements))


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
    await state.update_data(start_date=callback.data, end_date=callback.data)
    context_data = await state.get_data()
    await callback.message.edit_text(f"{template[LANG]['dateselect']}: {callback.data}")
    await callback.answer()
    await state.set_state(OrderWork.choosing_work_time)
    await callback.message.answer(text=template[LANG]['timechoice'],
                                  reply_markup=kb.time_keyboard_fab(context_data['work_type'], callback.data))


@router_register.message(OrderWork.choosing_work_date)
async def callbacks_days_select_incorrectly(message: Message, state: FSMContext):
    """Function for reselecting a value in case of incorrect input from the client"""
    context_data = await state.get_data()
    await message.answer(f"Incorrect select\n\n{template[LANG]['datechoice']}",
                         reply_markup=kb.date_keyboard_fab(context_data['work_type']))


@router_register.callback_query(OrderWork.choosing_work_time, F.data.regexp(r"\d{1,2}:\d{2}"))
async def callbacks_time_select_fab(callback: CallbackQuery, state: FSMContext):
    """
        Function receives callback and save value in FSM context MemoryStorage
        Sends a response to the user of his choice
    """
    await state.update_data(start_time=callback.data, end_time=callback.data)
    await callback.message.edit_text(f"{template[LANG]['timeselect']}: {callback.data}")
    await callback.answer()
    user_data = await state.get_data()
    await state.clear()
    update_client_db(user_data['client_id'], user_data['client_name'], user_data['description'])
    new_order_id = create_order_db(**user_data)
    await callback.message.answer(text=template[LANG]['create'].format(id=new_order_id))


@router_register.message(OrderWork.choosing_work_time)
async def callbacks_time_select_incorrectly(message: Message, state: FSMContext):
    """Function for reselecting a value in case of incorrect input from the client"""
    context_data = await state.get_data()
    await message.answer(f"Incorrect select\n\n{template[LANG]['timechoice']}",
                         reply_markup=kb.time_keyboard_fab(context_data['work_type'], context_data['start_date']))


if __name__ == '__main__':
    pass
