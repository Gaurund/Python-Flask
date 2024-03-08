'''
Задание

Объедините студентов в команды по 2-5 человек в сессионных залах.

Необходимо создать базу данных для интернет-магазина.
База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля:
    id (PRIMARY KEY),
    имя,
    фамилия,
    адрес электронной почты
    и пароль.
• Таблица заказов должна содержать следующие поля:
    id (PRIMARY KEY),
    id пользователя (FOREIGN KEY),
    id товара (FOREIGN KEY),
    дата заказа
    и статус заказа.
• Таблица товаров должна содержать следующие поля:
    id (PRIMARY KEY),
    название,
    описание
    и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.

Данная промежуточная аттестация оценивается по системе "зачет" / "не зачет"

"Зачет" ставится, если Слушатель успешно выполнил задание.
"Незачет" ставится, если Слушатель не выполнил задание.

Критерии оценивания:
1 - Слушатель создал базу данных для интернет-магазина.
    База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
'''

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from faker import Faker
from typing import List

from sqlalchemy import ForeignKey

DATABASE_URL = 'sqlite:///project/home-work-06/shop.db'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("last_name", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(128), nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(128), nullable=False),
)

stock = sqlalchemy.Table(
    "stock",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(256)),
    sqlalchemy.Column("price", sqlalchemy.Integer, nullable=False)
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("stock_id", ForeignKey("stock.id"), nullable=False),
    sqlalchemy.Column("date", sqlalchemy.Date()),
    sqlalchemy.Column("state_id", ForeignKey("states.id"), nullable=False, default=1)
)

states = sqlalchemy.Table(
    "states",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("state", sqlalchemy.String(16))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

app = FastAPI()


class UserIn(BaseModel):
    first_name: str = Field(min_length=2, max_length=32)
    last_name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=128)
    password: str = Field(max_length=128)


class User(UserIn):
    id: int


class StockIn(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=256)
    price: int


class Stock(StockIn):
    id: int


class Order(BaseModel):
    id: int
    user_id: int
    stock_id: int
    date: date
    state_id: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/fake_users/{count}")
async def create_fake_user(count: int):
    fake = Faker("ru_RU")
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.ascii_email()
        password = fake.ssn()
        query = users.insert().values(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password)
        await database.execute(query)
    return {'message': f'{count} fake users created'}


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.get("/shop/", response_model=List[Stock])
async def read_shop():
    query = stock.select()
    return await database.fetch_all(query)


@app.get("/shop/{stock_id}", response_model=Stock)
async def get_stock(stock_id: int):
    query = stock.select().where(stock.c.id == stock_id)
    return await database.fetch_one(query)


@app.post("/shop/", response_model=Stock)
async def create_stock(new_stock: StockIn):
    query = stock.insert().values(
        name=new_stock.name,
        description=new_stock.description,
        price=new_stock.price,
    )
    last_record_id = await database.execute(query)
    return {**new_stock.dict(), "id": last_record_id}


@app.put("/shop/{stock_id}", response_model=Stock)
async def update_stock(stock_id: int, new_stock: StockIn):
    query = stock.update().where(stock.c.id == stock_id).values(**new_stock.dict())
    await database.execute(query)
    return {**new_stock.dict(), "id": stock_id}


@app.delete("/shop/{stock_id}")
async def delete_stock(stock_id: int):
    query = stock.update().where(stock.c.id == stock_id)
    await database.execute(query)
    return {'message': 'Goods deleted'}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post("/orders/", response_model=Order)
async def create_order(new_order: Order):
    query = stock.insert().values(
        user_id=new_order.user_id,
        stock_id=new_order.stock_id,
        date=new_order.date,
        state_id=1
    )
    last_record_id = await database.execute(query)
    return {**new_order.dict(), "id": last_record_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_stock(order_id: int, new_order: Order):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_stock(order_id: int):
    query = orders.update().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
