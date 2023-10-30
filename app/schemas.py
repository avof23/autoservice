"""
Schemas data for fastapi model
"""
from typing import Optional
import datetime

from pydantic import BaseModel


class PartBase(BaseModel):
    part_name: str
    part_number: str
    original_number: str | None
    price: float
    description: str | None
    compatibility: str | None


class Part(PartBase):
    id: int

    class Config:
        from_attributes = True


class PartCreate(PartBase):
    pass


class PartUpdate(PartBase):
    part_name: Optional[str] = None
    part_number: Optional[str] = None
    original_number: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    compatibility: Optional[str] = None


class WorkBase(BaseModel):
    work_name: str
    price: float
    norm_min: int
    for_selection: bool
    requirements: str
    description: str


class Work(WorkBase):
    id: int

    class Config:
        from_attributes = True


class WorkCreate(WorkBase):
    pass


class WorkUpdate(WorkBase):
    work_name: Optional[str] = None
    price: Optional[float] = None
    norm_min: Optional[int] = None
    for_selection: Optional[bool] = None
    requirements: Optional[str] = None
    description: Optional[str] = None


class MasterBase(BaseModel):
    master_name: str
    qualification: str


class Master(MasterBase):
    id: int

    class Config:
        from_attributes = True


class MasterCreate(MasterBase):
    pass


class MasterUpdate(MasterBase):
    master_name: Optional[str] = None
    qualification: Optional[str] = None


class ClientBase(BaseModel):
    name: str
    phone: str | None
    email: str | None
    auto: str | None
    number: str | None
    description: str | None


class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    auto: Optional[str] = None
    number: Optional[str] = None
    description: Optional[str] = None


class StatusBase(BaseModel):
    status: str


class Status(StatusBase):
    id: int


class ContentBase(BaseModel):
    quantity: int


class Content(ContentBase):
    id: int
    work: Optional[Work] = None
    part: Optional[Part] = None


class ContentCreate(ContentBase):
    work_id: Optional[int] = None
    part_id: Optional[int] = None


class ContentUpdate(ContentBase):
    work_id: Optional[int] = None
    part_id: Optional[int] = None

class OrderBase(BaseModel):
    start_date: datetime.datetime
    end_date: datetime.datetime
    credit_summ: float
    order_summ: float
    description: str | None


class Order(OrderBase):
    id: int
    status: Status
    master: Master
    client: Client

    class Config:
        from_attributes = True


class ContentOrder(OrderBase):
    id: int
    status: Status
    master: Master
    client: Client
    content: list[Content]

    class Config:
        from_attributes = True


class OrderUpdate(OrderBase):
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None
    credit_summ: Optional[float] = None
    order_summ: Optional[float] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
