'''
Задание №2
Создать веб-приложение на FastAPI, которое будет предоставлять API для
работы с базой данных пользователей. Пользователь должен иметь
следующие поля:
○ ID (автоматически генерируется при создании пользователя)
○ Имя (строка, не менее 2 символов)
○ Фамилия (строка, не менее 2 символов)
○ Дата рождения (строка в формате "YYYY-MM-DD")
○ Email (строка, валидный email)
○ Адрес (строка, не менее 5 символов)
API должен поддерживать следующие операции:
○ Добавление пользователя в базу данных
○ Получение списка всех пользователей в базе данных
○ Получение пользователя по ID
○ Обновление пользователя по ID
○ Удаление пользователя по ID
Приложение должно использовать базу данных SQLite3 для хранения
пользователей.
'''

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from faker import Faker
from typing import List
from datetime import date

DATABASE_URL = 'sqlite:///project/lesson-06/mydb62.db'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

fake = Faker("ru_RU")

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("last_name", sqlalchemy.String(32)),
    sqlalchemy.Column("birth_date", sqlalchemy.Date()),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("address", sqlalchemy.String(128)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)


class UserIn(BaseModel):
    first_name: str = Field(min_length=2, max_length=32)
    last_name: str = Field(min_length=2, max_length=32)
    birth_date: date = Field()
    email: EmailStr = Field(max_length=128)
    address: str = Field(max_length=128)


class User(UserIn):
    id: int


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/fake_users/{count}")
async def create_fake_user(count: int):
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        birth_date = fake.date_of_birth()
        email = fake.ascii_email()
        address = fake.street_address()
        query = users.insert().values(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            email=email,
            address=address)
        await database.execute(query)
    return {'message': f'{count} fake users created'}


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
            first_name=user.first_name,
            last_name=user.last_name,
            birth_date=user.birth_date,
            email=user.email,
            address=user.address)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
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
