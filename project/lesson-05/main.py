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

'''
Задание №2
Создать API для получения списка фильмов по жанру. 
Приложение должно иметь возможность получать 
список фильмов по заданному жанру.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Movie с полями
    id, title, description и genre.
Создайте список movies для хранения фильмов.
Создайте маршрут для получения списка фильмов по жанру (метод GET).
Реализуйте валидацию данных запроса и ответа.
'''

from fastapi import FastAPI
from pydantic import BaseModel
from random import choice

app = FastAPI()


class Movie(BaseModel):
    id: int
    title: str
    description: str
    genre: str


movies = []
genres = [
    "Ужасы",
    "Триллер",
    "Комедия",
    "Исторический",
    "Фантастика"
]

for i in range(0, 10):
    new_movie = Movie(
        id=i,
        title=f'Title {i}',
        description=f'Description {i}',
        genre=choice(genres)
    )
    movies.append(new_movie)


@app.get('/')
async def root():
    return movies


@app.get('/genre/{genre}')
async def get_by_genre(genre: str):
    result = []
    for movie in movies:
        if movie.genre == genre:
            result.append(movie)
    return result if result else {'message': 'No movies in such genre was found'}


@app.post('/new/')
async def create_movie(movie: Movie):
    movies.append(movie)
    return movies


@app.put('/movies/{movie_id}')
async def edit_movie(movie_id: int, movie: Movie):
    for e in movies:
        if e.id == movie_id:
            movies.remove(e)
            movies.append(movie)
            return movies
    return {'message': 'Movie not found'}


@app.delete('/delete/{movie_id}')
async def delete_movie(movie_id: int):
    for e in movies:
        if e.id == movie_id:
            movies.remove(e)
            return movies
    return {'message': 'Movie not found'}
