from flask import Flask, render_template

'''
Задание №1
Создать страницу, на которой будет кнопка "Нажми меня", при
нажатии на которую будет переход на другую страницу с
приветствием пользователя по имени.
'''

app = Flask(__name__)


@app.route('/')
def index():
    context = {'title': 'index'}
    return render_template('index.html', **context)


@app.route('/hello/')
def hello():
    context = {'title': 'Hello!'}
    return render_template('hello.html', **context)


app.run()
