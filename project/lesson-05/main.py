'''
Задание №1.
Создать API для управления списком задач. Приложение должно иметь
возможность создавать, обновлять, удалять и получать список задач.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Task с полями id, title, description и status.
Создайте список tasks для хранения задач.
Создайте маршрут для получения списка задач (метод GET).
Создайте маршрут для создания новой задачи (метод POST).
Создайте маршрут для обновления задачи (метод PUT).
Создайте маршрут для удаления задачи (метод DELETE).
Реализуйте валидацию данных запроса и ответа.
'''

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


tasks = []

for i in range(0, 10):
    new_task = Task(
        id=i,
        title=f'Title {i}',
        description=f'Description {i}',
        status=f'Status {i}'
    )
    tasks.append(new_task)


@app.get('/')
async def root():
    return tasks


@app.post('/new/')
async def create_task(task: Task):
    tasks.append(task)
    return tasks


@app.put('/task/{task_id}')
async def change_task(task_id: int, task: Task):
    for e in tasks:
        if e.id == task_id:
            tasks.remove(e)
            tasks.append(task)
            # e = task
            return tasks
    return {'message': 'Task not found'}


@app.delete('/delete/{task_id}')
async def delete_task(task_id: int):
    for e in tasks:
        if e.id == task_id:
            tasks.remove(e)
            return tasks
    return {'message': 'Task not found'}