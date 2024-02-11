from flask import Flask

'''
Задание №1
Напишите простое веб-приложение на Flask, которое будет
выводить на экран текст "Hello, World!".
'''

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def index():
    return 'Hello world'


if __name__ == '__main__':
    app.run()
