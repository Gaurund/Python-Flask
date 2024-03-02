'''
Необходимо создать API для управления списком задач.
Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность
указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу
  с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу
  с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу
  с указанным идентификатором.

Для каждой конечной точки необходимо
проводить валидацию данных запроса и ответа.
Для этого использовать библиотеку Pydantic.
'''

from fastapi import FastAPI
from pydantic import BaseModel
from random import choice

app = FastAPI()


class Task(BaseModel):
    id: int
    name: str
    description: str
    status: str


statuses = ['выполнена', 'не выполнена']


def fill_tasks():
    tasks_ = []
    for i in range(0, 10):
        new_task = Task(
            id=i,
            name=f'Title {i}',
            description=f'Description {i}',
            status=choice(statuses)
        )
        tasks_.append(new_task)
    return tasks_


tasks = fill_tasks()


@app.get('/tasks')
async def get_tasks():
    return tasks


@app.get('/tasks/{id}')
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return {'message': 'No such task in the list was found.'}


@app.post('/tasks')
async def add_task(task: Task):
    for e in tasks:
        if e.id == task.id:
            return {'message': 'A task with the id exists already. No changes were made.'}
    tasks.append(task)
    return {'message': 'The task was added in the list.'}


@app.put('/tasks/{id}')
async def edit_task(task_id: int, new_task: Task):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            tasks.append(new_task)
            return {'message': 'The task has been changed.'}
    return {'message': 'No such task in the list was found.'}


@app.delete('/tasks/{id}')
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {'message': 'The task has been deleted.'}
    return {'message': 'No such task in the list was found.'}

