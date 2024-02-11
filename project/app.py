from flask import Flask

'''
Задание №1
Напишите простое веб-приложение на Flask, которое будет
выводить на экран текст "Hello, World!".
'''

'''
Задание №2
Дорабатываем задачу 1.
Добавьте две дополнительные страницы в ваше вебприложение:
○ страницу "about"
○ страницу "contact".
'''

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def index():
    return 'Hello world'


@app.route('/about/')
def about():
    return "About me"


@app.route('/contacts/')
def contacts():
    return "My contacts"


if __name__ == '__main__':
    app.run()
