from flask import Flask, render_template, request, flash

'''
Задание 

Создать страницу, на которой будет форма для ввода
имени и электронной почты, при отправке которой
будет создан cookie-файл с данными пользователя,
а также будет произведено перенаправление
на страницу приветствия, где будет отображаться имя пользователя.

На странице приветствия должна быть кнопка «Выйти»,
 при нажатии на которую будет удалён cookie-файл
 с данными пользователя и произведено перенаправление
 на страницу ввода имени и электронной почты.
'''

app = Flask(__name__)


@app.route('/')
def index():
    context = {'title': 'Вход'}
    return render_template('index.html', **context)


@app.post('/submit')
def submit_post():
    name = request.form.get('name')
    return f'Hello {name}'


@app.get('/submit')
def submit_get():
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
