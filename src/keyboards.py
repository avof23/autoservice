from sqlalchemy.orm import Session
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from db import engine, Works
from constants import LANG
from text_templates import template


class WorksCallbackFactory(CallbackData, prefix="fabwork"):
    id: int
    work_name: str
    price: float
    norm_min: int


def kbselect_db_works() -> list:
    """Function get information about works from database
       Returns:
           List: Information about works in dictionary
       """
    with Session(engine) as session:
        q_result = session.query(Works).filter(
            Works.for_selection == True).all()
    return q_result

def works_keyboard_fab():
    """Function generate Inline keyboard for select works in chat
    Returns:
        InlineKeyboardBuilder markup"""
    kb_works = InlineKeyboardBuilder()
    for work in kbselect_db_works():
        kb_works.button(text=work.work_name,
                        callback_data=WorksCallbackFactory(id=work.id,
                                                           work_name=work.work_name,
                                                           price=work.price,
                                                           norm_min=work.norm_min))

    kb_works.adjust(1)
    return kb_works.as_markup()


#Reply Keyboard with bilder
# kb_works = ReplyKeyboardBuilder()
# for work in kbselect_db_works():
#     kb_works.add(KeyboardButton(text=work.work_name))
# kb_works.adjust(1)

# Reply Keyboard without bilder
#kb = [[KeyboardButton(text=work.work_name)] for work in kbselect_db_works()]
#greet_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
#                                   input_field_placeholder=template[LANG]['workselect'])


if __name__ == '__main__':
    for work in kbselect_db_works():
        print(work)
