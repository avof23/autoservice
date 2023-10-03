"""This module for connecting to a database to receive and update the status of orders to be sent push message"""

from datetime import datetime as dt, timedelta

from sqlalchemy.orm import Session
from db import engine, Orders


def get_recipients_db(order_type: int) -> list:
    """
    The function receives orders from the database by their type
    :param order_type: int for filtering database select
    :return: List contains dict orders
    """
    now = dt.now()
    now += timedelta(days=1)
    with Session(engine) as session:
        rp_result = session.query(Orders).filter(Orders.status_id == order_type)
        if order_type == 1:
            rp_result = rp_result.filter(Orders.start_date < now)
        rp_result.all()
        result = [{
            'id': order.id,
            'status': order.status.status,
            'client_id': order.client_id,
            'start_date': dt.strftime(order.start_date, '%d.%m.%Y %H:%M'),
            'master': order.master.master_name
        } for order in rp_result]
    return result


def set_pushed_db(ids: list) -> None:
    """
    The function changes the status of an order in the database by its ID
    :param ids: list contains id for changed in database
    :return: None
    """
    with Session(engine) as session:
        for order_id in ids:
            updated_id = session.query(Orders).filter(Orders.id == order_id).first()
            updated_id.status_id = int(updated_id.status_id) + 1
        session.commit()


if __name__ == "__main__":
    for od in get_recipients_db(1):
        print(od)
