"""Router module for API requests works from database
GET Default limit parameters skip=0, limit=20
POST for create new work
PATCH for update some attributes"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.db import engine, Works
from app import schemas

router = APIRouter()


@router.get("", response_model=list[schemas.Work])
async def get_works(skip: int = 0, limit: int = 20) -> list:
    """
    Function to get work items from the database
    :param skip: int how many items skip
    :param limit: int now many items get from database
    :return: list of works from database
    """
    with Session(engine) as session:
        works = session.query(Works).offset(skip).limit(limit).all()
    return works


@router.get("/{work_id}", response_model=schemas.Work)
async def get_work(work_id: int) -> type[Works]:
    """
    Function to get work item by ID from the database
    :param work_id: int id for filter request
    :return: list Object Works from model
    """
    with Session(engine) as session:
        work = session.get(Works, work_id)
    if work is None:
        raise HTTPException(status_code=404, detail="Work not found")
    return work


@router.post("", response_model=schemas.Work)
async def create_work(work: schemas.WorkCreate) -> dict:
    """
    Function create work item in database
    :param work: Object WorkCreate from schema
    :return: dict of attributes created work
    """
    db_work = Works(**work.model_dump())
    with Session(engine) as session:
        session.add(db_work)
        session.commit()
        session.refresh(db_work)
        return db_work


@router.patch("/{work_id}", response_model=schemas.Work)
async def update_work(work_id: int, work: schemas.WorkUpdate) -> type[Works]:
    """
    Function update work item in database
    Сan update individual attributes of work
    :param work_id: int id for filter request
    :param work: Object WorkUpdate from schema
    :return: list Object Works from model
    """
    with Session(engine) as session:
        stored_work = session.get(Works, work_id)
        if stored_work is None:
            raise HTTPException(status_code=404, detail="Work not found")
        update_data = work.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(stored_work, key, value)

        session.commit()
        session.refresh(stored_work)
        return stored_work
