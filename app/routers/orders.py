"""Router module for API requests orders from database
GET Default limit parameters skip=0, limit=20
PATCH for update some attributes"""
import datetime
from datetime import datetime as dt

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.db import engine, Orders, ContentOrders
from app import schemas

router = APIRouter()


@router.get("", response_model=list[schemas.Order])
async def get_orders(from_date: str = dt.strftime(dt.now() - datetime.timedelta(days=7), '%Y-%m-%d 00:00'),
                     to_date: str = dt.strftime(dt.now(), '%Y-%m-%d 23:59'),
                     master_id: int = 0,
                     client_id: int = 0,
                     skip: int = 0,
                     limit: int = 20) -> list:
    """
    Function to get orders items from the database
    :param from_date: datetime for filter query result
    :param to_date: datetime for filter query result
    :param master_id: int for filter query result
    :param client_id: int for filter query result
    :param skip: int how many items skip
    :param limit: int now many items get from database
    :return: list of orders from database
    """
    with Session(engine) as session:
        orders = session.query(Orders)\
            .filter(Orders.start_date >= from_date)\
            .filter(Orders.end_date <= to_date)
        if master_id:
            orders = orders.filter(Orders.master_id == master_id)
        if client_id:
            orders = orders.filter(Orders.client_id == client_id)
        orders = orders.offset(skip).limit(limit).all()
        result = [{
            'id': order.id,
            'status': order.status,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'order_summ': order.order_summ,
            'credit_summ': order.credit_summ,
            'master': order.master,
            'client': order.client,
            'description': order.description
        } for order in orders]
    return result


@router.get("/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int) -> dict:
    """
    Function to get order item by ID from the database
    :param order_id: int id for filter request
    :return: dict Order + content order
    """
    with Session(engine) as session:
        order = session.get(Orders, order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        result = {
            'id': order.id,
            'status': order.status,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'order_summ': order.order_summ,
            'credit_summ': order.credit_summ,
            'master': order.master,
            'client': order.client,
            'description': order.description,
        }
    return result


@router.get("/with_content/{order_id}", response_model=schemas.ContentOrder)
async def get_order_with_content(order_id: int) -> dict:
    """
    Function to get order item by ID from the database
    :param order_id: int id for filter request
    :return: dict Order + content order
    """
    with Session(engine) as session:
        order = session.query(Orders).filter(Orders.id == order_id).first()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        order_cont = session.query(ContentOrders).filter(ContentOrders.order_id == order_id).all()

        result = {
            'id': order.id,
            'status': order.status,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'order_summ': order.order_summ,
            'credit_summ': order.credit_summ,
            'master': order.master,
            'client': order.client,
            'description': order.description,
            'content': order_cont
        }
    return result


@router.patch("/{order_id}", response_model=schemas.Order)
async def update_order(order_id: int, order: schemas.OrderUpdate) -> type[Orders]:
    """
    Function update order item in database
    Сan update some individual attributes of order
    :param order_id: int id for filter request
    :param order: Object OrderUpdate from schema
    :return: list Object Order from model
    """
    with Session(engine) as session:
        stored_order = session.get(Orders, order_id)
        if stored_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        update_data = order.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(stored_order, key, value)

        session.commit()
        session.refresh(stored_order)
        return stored_order


@router.post("/content/{order_id}", response_model=schemas.ContentCreate)
async def create_order_content(order_id: int, cont: schemas.ContentCreate) -> dict:
    db_content = ContentOrders(**cont.model_dump())
    db_content.order_id = order_id
    if db_content.part_id == 0:
        db_content.part_id = None
    if db_content.work_id == 0:
        db_content.work_id = None
    with Session(engine) as session:
        session.add(db_content)
        session.commit()
        session.refresh(db_content)
        return db_content


@router.patch("/content/{cont_id}", response_model=schemas.ContentUpdate)
async def update_order_content(cont_id: int, cont: schemas.ContentUpdate) -> type[ContentOrders]:
    with Session(engine) as session:
        stored_content = session.get(ContentOrders, cont_id)
        if stored_content is None:
            raise HTTPException(status_code=404, detail="Content not found")
        update_data = cont.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(stored_content, key, value)

        if stored_content.part_id == 0:
            stored_content.part_id = None
        if stored_content.work_id == 0:
            stored_content.work_id = None

        session.commit()
        session.refresh(stored_content)
        return stored_content


@router.delete("/content/{cont_id}")
async def delete_order_content(cont_id: int) -> str:
    with Session(engine) as session:
        db_content = session.get(ContentOrders, cont_id)
        if db_content is None:
            raise HTTPException(status_code=404, detail="Content not found")
        session.delete(db_content)
        session.commit()
        return f"successful deleted content {cont_id} from order {db_content.order_id}"
