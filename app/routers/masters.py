"""Router module for API requests masters from database
GET Default limit parameters skip=0, limit=20
POST for create new master
PATCH for update some attributes"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.db import engine, Masters
from app import schemas

router = APIRouter()


@router.get("", response_model=list[schemas.Master])
async def get_masters(skip: int = 0, limit: int = 20) -> list:
    """
    Function to get master items from the database
    :param skip: int how many items skip
    :param limit: int now many items get from database
    :return: list of masters from database
    """
    with Session(engine) as session:
        masters = session.query(Masters).offset(skip).limit(limit).all()
    return masters


@router.get("/{master_id}", response_model=schemas.Master)
async def get_master(master_id: int) -> type[Masters]:
    """
    Function to get master item by ID from the database
    :param master_id: int id for filter request
    :return: list Object Masters from model
    """
    with Session(engine) as session:
        master = session.get(Masters, master_id)
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return master


@router.post("", response_model=schemas.Master)
async def create_master(master: schemas.MasterCreate) -> dict:
    """
    Function create master item in database
    :param master: Object MasterCreate from schema
    :return: dict of attributes created master
    """
    db_master = Masters(**master.model_dump())
    with Session(engine) as session:
        session.add(db_master)
        session.commit()
        session.refresh(db_master)
        return db_master


@router.patch("/{master_id}", response_model=schemas.Master)
async def update_master(master_id: int, master: schemas.MasterUpdate) -> type[Masters]:
    """
    Function update master item in database
    Сan update individual attributes of master
    :param master_id: int id for filter request
    :param master: Object MasterUpdate from schema
    :return: list Object Master from model
    """
    with Session(engine) as session:
        stored_master = session.get(Masters, master_id)
        if stored_master is None:
            raise HTTPException(status_code=404, detail="Master not found")
        update_data = master.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(stored_master, key, value)

        session.commit()
        session.refresh(stored_master)
        return stored_master
