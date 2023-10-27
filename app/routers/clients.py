"""Router module for API requests clients from database
GET Default limit parameters skip=0, limit=20
POST for create new client
PATCH for update some attributes"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.db import engine, Clients
from app import schemas

router = APIRouter()


@router.get("", response_model=list[schemas.Client])
async def get_clients(skip: int = 0, limit: int = 20) -> list:
    """
    Function to get clients items from the database
    :param skip: int how many items skip
    :param limit: int now many items get from database
    :return: list of clients from database
    """
    with Session(engine) as session:
        clients = session.query(Clients).offset(skip).limit(limit).all()
    return clients


@router.get("/{client_id}", response_model=schemas.Client)
async def get_client(client_id: int) -> type[Clients]:
    """
    Function to get client item by ID from the database
    :param client_id: int id for filter request
    :return: list Object Clients from model
    """
    with Session(engine) as session:
        client = session.get(Clients, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("", response_model=schemas.Client)
async def create_client(client: schemas.ClientCreate) -> dict:
    """
    Function create client item in database
    :param client: Object ClientCreate from schema
    :return: dict of attributes created client
    """
    db_client = Clients(**client.model_dump())
    with Session(engine) as session:
        session.add(db_client)
        session.commit()
        session.refresh(db_client)
        return db_client


@router.patch("/{client_id}", response_model=schemas.Client)
async def update_client(client_id: int, client: schemas.ClientUpdate) -> type[Clients]:
    """
    Function update client item in database
    Сan update individual attributes of client
    :param client_id: int id for filter request
    :param client: Object ClientUpdate from schema
    :return: list Object Client from model
    """
    with Session(engine) as session:
        stored_client = session.get(Clients, client_id)
        if stored_client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        update_data = client.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(stored_client, key, value)

        session.commit()
        session.refresh(stored_client)
        return stored_client
