from flask import Flask, make_response, render_template, request, flash, redirect, url_for

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
app.secret_key = b'94dc38deee56cf4e4e64530d5c9d09f3e6295e7ee7c3811eb8c2c88f8d76b0db'


@app.route('/')
def index():
    context = {
        'title': 'Вход'
    }
    return render_template('index.html', **context)


@app.route('/hello/', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return redirect(url_for('index'))
    if not request.form['name']:
        flash('Необходимо ввести имя...', 'danger')
        return redirect(url_for('index'))
    if not request.form['email']:
        flash('Необходимо ввести почту...', 'danger')
        return redirect(url_for('index'))

    name = request.form.get('name')
    email = request.form.get('email')
    context = {
        'title': 'Приветствие',
        'name': name,
        'email': email
    }
    response = make_response(render_template('hello.html', **context))
    response.set_cookie('username', name)
    response.set_cookie('email', email)
    return response


@app.route('/delete_cookies/')
def delete_cookies():
    context = {
        'title': 'Прощание'
    }
    flash('Кукисы успешно удалены. До свидания!', 'success')
    response = make_response(render_template('index.html', **context))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


if __name__ == '__main__':
    app.run(debug=True)
