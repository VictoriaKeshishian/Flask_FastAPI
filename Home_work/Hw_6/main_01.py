
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException
from typing import List
from Home_work.Hw_6.models_01 import User, UserIn, ItemIn, Item, OrderIn, Order


DATABASE_URL = "sqlite:///hw6_database.db"


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("lastname", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)

items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("item_name", sqlalchemy.String(128)),
    sqlalchemy.Column("description", sqlalchemy.String(200)),
    sqlalchemy.Column("cost", sqlalchemy.DECIMAL),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("id_user", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("id_item", sqlalchemy.Integer, sqlalchemy.ForeignKey('items.id')),
    sqlalchemy.Column("date", sqlalchemy.DateTime()),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, lastname=user.lastname, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/items/", response_model=Item)
async def create_item(item: ItemIn):
    query = items.insert().values(item_name=item.item_name, description=item.description, cost=item.cost)
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}


@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    query = items.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    query = items.select().where(items.c.id == item_id)
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(id_user=order.id_user, id_item=order.id_item, date=order.date, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders(skip: int = 0, limit: int = 10):
    query = orders.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {"message": "Item deleted successfully"}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemIn):
    query = (
        items.update()
        .where(items.c.id == item_id)
        .values(item_name=item.item_name, description=item.description, cost=item.cost)
    )
    await database.execute(query)
    return {"message": "Item updated successfully"}
