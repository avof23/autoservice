
from sqlalchemy.orm import Session
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from db import engine, Orders

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
            Orders.id == order_id).all()
        result = {
            'id': q_result[0].id,
            'status': q_result[0].status.status,
            'start_date': q_result[0].start_date,
            'end_date': q_result[0].end_date,
            'order_summ': q_result[0].order_summ,
            'master': q_result[0].master.master_name,
            'descr': q_result[0].description
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
            answer_message = 'Order ID: {id}\n' \
                             'Status: {status} Start in: {start_date}\n' \
                             'Summ: {order_summ} Master name: {master}'.format(**order_info)
            await message.answer(answer_message)
        except Exception:
            await message.answer('Incorrect Order ID!')
    else:
        await message.answer('Please enter your Order ID\n after command /status')


if __name__ == '__main__':
    try:
        inp_id = int(input('Enter ID:'))
        print(get_db_order(inp_id))
    except Exception:
        print('Incorrect ID')
