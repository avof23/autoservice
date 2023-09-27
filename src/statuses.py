"""This module creates a router that processes status requests from users"""
from datetime import datetime as dt

from sqlalchemy.orm import Session
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandObject
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from db import engine, Orders, ContentOrders, Works, Parts
from constants import LANG, VALUT, template


router_status = Router()


def get_db_order(user_id: int, order_id: int | bool = False) -> list:
    """
    Function get information about order id from database
    :param
        user_id: Integer for filter by user ID in query
        order_id: Integer or bool for width filter by order ID in query
    :return: List: Information about order in dictionary
    """
    with Session(engine) as session:
        q_result = session.query(Orders)
        if order_id:
            q_result = q_result.filter(Orders.id == order_id, Orders.client_id == user_id)
        else:
            q_result = q_result.filter(Orders.client_id == user_id).filter(Orders.status_id <= 4)
        q_result.all()
        result = [{
            'id': order.id,
            'status': order.status.status,
            'start_date': dt.strftime(order.start_date, '%d.%m.%Y %H:%M'),
            'end_date': order.end_date,
            'order_summ': f"{order.order_summ} {VALUT}",
            'credit_summ': f"{int(order.credit_summ) * (-1)} {VALUT}",
            'master': order.master.master_name,
            'descr': order.description
        } for order in q_result]
    return result


def get_context_order(order_id: int) -> list:
    """
    The Function get from db list works and list part for order ID
    :param order_id: Int Oders ID for filter in database
    :return: List contain work and part for order
    """
    with Session(engine) as session:
        q_contwork = session.query(ContentOrders.order_id, ContentOrders.quantity, Works.work_name, Works.price,)\
            .join(Works).filter(ContentOrders.order_id == order_id)
        q_contwork.all()
        q_contpart = session.query(ContentOrders.order_id, ContentOrders.quantity, Parts.part_name, Parts.price) \
            .join(Parts).filter(ContentOrders.order_id == order_id)
        q_contpart.all()
        resultw = [{'name': contw.work_name,
                    'qt': contw.quantity,
                    'price': contw.price} for contw in q_contwork]
        resultp = [{'name': contp.part_name,
                    'qt': contp.quantity,
                    'price': contp.price} for contp in q_contpart]
    return resultw + resultp


@router_status.message(Command("info", ignore_case=True))
async def get_invoice(message: Message, command: CommandObject):
    def generate_pdf(oid: int, oinf: list) -> None:
        """
        Helper function generate pdf
        :param oid: order ID
        :param oinf: list order information
        :return: None
        """
        my_canvas = canvas.Canvas(f"../data/invoice_{oid}.pdf")
        my_canvas.setTitle('Invoice document PyAutoService')
        my_canvas.drawImage('../img/pyLogo.png', 30, 700, width=100, height=100, preserveAspectRatio=True, mask='auto')
        my_canvas.setFont('Helvetica', 14)
        my_canvas.drawString(150, 750, 'PyAutoService')
        my_canvas.setLineWidth(.3)
        my_canvas.setFont('Helvetica', 12)
        my_canvas.drawString(30, 650, f'INVOICE # {oid}')
        my_canvas.drawString(30, 635, f'CUSTOMER: {message.from_user.full_name}')
        my_canvas.drawString(350, 650, f"DATE: {oinf[0]['start_date']}")
        my_canvas.line(390, 647, 580, 647)
        my_canvas.drawString(350, 625, 'TOTAL AMOUNT:')
        my_canvas.drawString(450, 625, f"{oinf[0]['order_summ']}")
        my_canvas.line(450, 623, 580, 623)
        my_canvas.drawString(30, 603, 'RECEIVED BY:')
        my_canvas.line(120, 600, 580, 600)
        my_canvas.drawString(120, 603, "PyAutoService")
        my_canvas.setLineWidth(.3)

        i = 1
        total = 0
        data = [
            ['#', 'Position', 'Qt', 'Price', 'Summ'],
        ]
        for item in get_context_order(oid):
            data.append([i, item['name'], item['qt'], item['price'], item['qt'] * item['price']])
            total += item['qt'] * item['price']
            i += 1
        data.append(['', '', '', 'TOTAL:', f'{total} {VALUT}'])

        tblstyle = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),
            ('BOX', (3, -1), (4, -1), 1, colors.black),
        ])
        tbl = Table(data, colWidths=[30, 260, 70, 70, 70])
        tbl.setStyle(tblstyle)
        tbl.wrapOn(my_canvas, 500, len(data) * 50)
        tbl.drawOn(my_canvas, 30, 450)
        my_canvas.save()

    if command.args:
        try:
            order_id = int(command.args)
            order_info = get_db_order(message.from_user.id, order_id)
            generate_pdf(order_id, order_info)
            file = FSInputFile(f"../data/invoice_{order_id}.pdf", filename=f"invoice_{order_id}.pdf")
            await message.answer_document(file)
        except Exception:
            await message.answer(template[LANG]['incorrectid'])


@router_status.message(Command("status", ignore_case=True))
async def get_status(message: Message, command: CommandObject) -> None:
    """This handler receives messages with `/status` command,
    get id from user. Return information about order"""
    if command.args:
        try:
            order_id = int(command.args)
            order_info = get_db_order(message.from_user.id, order_id)
            answer_message = template[LANG]['answerorder'].format(**order_info[0])
            await message.answer(answer_message)
        except Exception:
            await message.answer(template[LANG]['incorrectid'])
    else:
        if len(client_orders := get_db_order(message.from_user.id)) > 0:
            await message.answer(template[LANG]['multiorder'])
            for order in client_orders:
                answer_message = template[LANG]['answerorder'].format(**order)
                await message.answer(answer_message)
        else:
            await message.answer(template[LANG]['orderreq'])


if __name__ == '__main__':
    try:
        ord_id = int(input('Enter Order ID:'))
        if ord_id == 0:
            ord_id = False
        usr_id = int(input('Enter User ID:'))
        print(get_db_order(usr_id, ord_id))
    except Exception:
        print('Incorrect ID')
