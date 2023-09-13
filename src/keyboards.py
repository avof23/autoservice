"""This module describes and creates all keyboards for dialogue with the user"""
import datetime

from sqlalchemy.orm import Session
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from db import engine, Works
from constants import WEEKEND_DAYS, WORK_TIME


class WorksCallbackFactory(CallbackData, prefix="fabwork"):
    """The class describes the callback request format of works selected by the user"""
    id: int
    work_name: str
    price: float
    norm_min: int


def get_works_db() -> list:
    """Function get information about works from database
       Returns:
           List: Information about works in dictionary
       """
    with Session(engine) as session:
        q_result = session.query(Works).filter(
            Works.for_selection == True).all()
    return q_result


def get_days() -> list:
    """The function determines the nearest working days from the current one,
    taking into account weekends
    Returns:
        list: work days format DD.MM"""
    now = datetime.datetime.now()
    days_for_reg = []
    while len(days_for_reg) < 7 - len(WEEKEND_DAYS):
        if int(now.strftime('%w')) in WEEKEND_DAYS:
            now += datetime.timedelta(days=1)
            continue
        days_for_reg.append(now.strftime('%d.%m'))
        now += datetime.timedelta(days=1)
    return days_for_reg


def works_keyboard_fab():
    """Function generate Inline keyboard for select works in chat
    Returns:
        InlineKeyboardBuilder markup"""
    kb_works = InlineKeyboardBuilder()
    for work in get_works_db():
        kb_works.button(text=work.work_name,
                        callback_data=WorksCallbackFactory(id=work.id,
                                                           work_name=work.work_name,
                                                           price=work.price,
                                                           norm_min=work.norm_min))
    kb_works.adjust(1)
    return kb_works.as_markup()


def date_keyboard_fab():
    """Function generate Inline keyboard for select date in chat"""
    kb_date = InlineKeyboardBuilder()
    for day in get_days():
        kb_date.button(text=day, callback_data=day)
    kb_date.adjust(2)
    return kb_date.as_markup()


def time_keyboard_fab():
    """Function generate Inline keyboard for select time in chat"""
    kb_time = InlineKeyboardBuilder()
    for hour in WORK_TIME:
        kb_time.button(text=f'{hour}:00', callback_data=f'{hour}:00')
    kb_time.adjust(3)
    return kb_time.as_markup()


if __name__ == '__main__':
    for work in get_works_db():
        print(work)
