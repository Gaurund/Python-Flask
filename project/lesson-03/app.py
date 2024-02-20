import random

from flask import Flask, render_template
from models import *

'''
Задание №1

Создать базу данных для хранения информации о студентах университета.
База данных должна содержать две таблицы: "Студенты" и "Факультеты".
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия,
возраст, пол, группа и id факультета.
В таблице "Факультеты" должны быть следующие поля: id и название
факультета.
Необходимо создать связь между таблицами "Студенты" и "Факультеты".
Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их факультета.
'''

'''
Задание №2
Создать базу данных для хранения информации о книгах в библиотеке.
База данных должна содержать две таблицы: "Книги" и "Авторы".
В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
Необходимо создать связь между таблицами "Книги" и "Авторы".
Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = b'cf1d7e9578733c0ad1c040e081cd19b542bed43e98dab1d22abd0fbfe2fe71f8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'

db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.cli.command('fill-t1')
def fill_task1_tables():
    for i in range(1, 6):
        new_faculty = Faculty(
            name=f'Faculty{i}'
        )
        db.session.add(new_faculty)
    db.session.commit()

    for i in range(1, 11):
        new_student = Student(
            first_name=f'First_name{i}',
            last_name=f'Last_name{i}',
            age=random.randint(10, 90),
            gender=random.choice([True, False]),
            group=random.randint(100, 200),
            faculty_id=random.randint(1, 5)
        )
        db.session.add(new_student)
    db.session.commit()
    print('OK')


@app.route('/')
@app.route('/index/')
def index():
    students = Student.query.all()
    context = {
        'students': students,
        'title': 'Студентики'
    }
    return render_template('task1.html', **context)


def result(message):
    return render_template('result.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
