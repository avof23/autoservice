"""This module creates a router that processes status requests from users"""
from sqlalchemy.orm import Session
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from db import engine, Orders
from constants import LANG, template


router_status = Router()


def get_db_order(order_id: int) -> dict:
    """Function get information about order id from database
    Parameters:
        order_id: Integer for width filter in query
    Returns:
        List: Information about order in dictionary
    """
    with Session(engine) as session:
        q_result = session.query(Orders).filter(
            Orders.id == order_id).first()
        result = {
            'id': q_result.id,
            'status': q_result.status.status,
            'start_date': q_result.start_date,
            'end_date': q_result.end_date,
            'order_summ': q_result.order_summ,
            'master': q_result.master.master_name,
            'descr': q_result.description
        }
    return result


@router_status.message(Command("status", ignore_case=True))
async def get_status(message: Message, command: CommandObject) -> None:
    """This handler receives messages with `/status` command,
    get id from user. Return information about order"""
    if command.args:
        try:
            order_id = int(command.args)
            order_info = get_db_order(order_id)
            answer_message = template[LANG]['answerorder'].format(**order_info)
            await message.answer(answer_message)
        except Exception:
            await message.answer(template[LANG]['incorrectid'])
    else:
        await message.answer(template[LANG]['orderreq'])


if __name__ == '__main__':
    try:
        inp_id = int(input('Enter ID:'))
        print(get_db_order(inp_id))
    except Exception:
        print('Incorrect ID')
