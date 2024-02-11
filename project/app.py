from flask import Flask, render_template

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

'''
Задание №3
Написать функцию, которая будет принимать на вход два
числа и выводить на экран их сумму.
'''

'''
Задание №4
Написать функцию, которая будет принимать на вход строку и
выводить на экран ее длину.
'''

'''
Задание №5
Написать функцию, которая будет выводить на экран HTML
страницу с заголовком "Моя первая HTML страница" и
абзацем "Привет, мир!".
'''


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return "About me"


@app.route('/contacts/')
def contacts():
    return "My contacts"


@app.route('/<int:number1>+<int:number2>')
def sum_numbers(number1, number2):
    return str(number1 + number2)


@app.route('/<string:line>')
def length(line):
    return str(len(line))


if __name__ == '__main__':
    app.run()
