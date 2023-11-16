"""Router module for API requests parts from database
GET Default limit parameters skip=0, limit=20
POST for create new part
PATCH for update some attributes"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.db import engine, Parts
from app import schemas

router = APIRouter()


@router.get("", response_model=list[schemas.Part])
async def get_parts(skip: int = 0, limit: int = 20) -> list:
    """
    Function to get part items from the database
    :param skip: int how many items skip
    :param limit: int now many items get from database
    :return: list of parts from database
    """
    with Session(engine) as session:
        parts = session.query(Parts).offset(skip).limit(limit).all()
    return parts


@router.get("/{part_id}", response_model=schemas.Part)
async def get_part(part_id: int) -> type[Parts]:
    """
    Function to get part item by ID from the database
    :param part_id: int id for filter request
    :return: list Object Parts from model
    """
    with Session(engine) as session:
        part = session.get(Parts, part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return part


@router.post("", response_model=schemas.Part)
async def create_part(part: schemas.PartCreate) -> dict:
    """
    Function create part item in database
    :param part: Object PartCreate from schema
    :return: dict of attributes created part
    """
    db_part = Parts(**part.model_dump())
    with Session(engine) as session:
        session.add(db_part)
        session.commit()
        session.refresh(db_part)
        return db_part


@router.patch("/{part_id}", response_model=schemas.Part)
async def update_part(part_id: int, part: schemas.PartUpdate) -> type[Parts]:
    """
    Function update part item in database
    Сan update individual attributes of part
    :param part_id: int id for filter request
    :param part: Object PartUpdate from schema
    :return: list Object Parts from model
    """
    with Session(engine) as session:
        stored_part = session.get(Parts, part_id)
        if stored_part is None:
            raise HTTPException(status_code=404, detail="Part not found")
        update_data = part.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(stored_part, key, value)

        session.commit()
        session.refresh(stored_part)
        return stored_part
