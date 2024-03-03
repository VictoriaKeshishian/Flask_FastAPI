from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    lastname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)


class ItemIn(BaseModel):
    item_name: str = Field(max_length=128)
    description: str = Field(max_length=200)
    cost: Decimal = Field()


class OrderIn(BaseModel):
    id_user: int
    id_item: int
    date: datetime = Field(default_factory=datetime.now)
    status: bool = False


class User(UserIn):
    id: int


class Item(ItemIn):
    id: int


class Order(OrderIn):
    id: int

