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


@app.route('/sumbit', methods=['GET', 'POST'])
def submit():
    context = {'title': 'Добро пожаловать'}
    if request.method == 'POST':
        if not request.form['user-name']:
            flash("Ввод имени обязателен!", "danger")
            return render_template('hello.html', **context)
        name = request.form.get('name')
        context['name'] = name
        return render_template('hello.html', **context)
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run()
