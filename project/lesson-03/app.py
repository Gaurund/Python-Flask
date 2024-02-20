from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import models

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

app = Flask(__name__)
app.config['SECRET_KEY'] = b'cf1d7e9578733c0ad1c040e081cd19b542bed43e98dab1d22abd0fbfe2fe71f8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
db = SQLAlchemy(app)

db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.cli.command('fill-t1')
def fill_task1_tables():
    for i in range(1, 11):
        new_student = models.Student()


@app.route('/')
@app.route('index')
def index():
    return render_template('index.html')


def result(message):
    return render_template('result.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
