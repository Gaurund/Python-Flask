from flask import Flask, render_template, request, flash, redirect, url_for

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
    context = {'title': 'Вход'}
    return render_template('index.html', **context)


@app.post('/submit')
def submit_post():
    name = request.form.get('name')
    return f'Hello {name}'


@app.get('/submit')
def submit_get():
    return render_template('form.html')


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('form'))
    return render_template('flash_form.html')


if __name__ == '__main__':
    app.run(debug=True)
