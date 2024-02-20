'''
Задание

Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля:
    "Имя",
    "Фамилия",
    "Email",
    "Пароль"
    и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться
в базе данных, а пароль должен быть зашифрован.
'''
from flask import Flask, render_template, request, url_for
from forms import LoginForm
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = b'bc554e95290c3a18549fd9c061750ca7dcd1dd794d4ebe4ae4c2e2d7709325af'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw3.db'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        context = {'users': users}
        return render_template('confirmation.html', **context)
    return render_template('index.html', form=form)


@app.route('/confirmation/')
def confirmation():
    users = User.query.all()
    context = {'users': users}
    return render_template('confirmation.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
