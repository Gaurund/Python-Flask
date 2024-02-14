from flask import Flask, render_template, url_for, request

'''
Задание №1
Создать страницу, на которой будет кнопка "Нажми меня", при
нажатии на которую будет переход на другую страницу с
приветствием пользователя по имени.
'''

'''
Задание №2
Создать страницу, на которой будет изображение и ссылка
на другую страницу, на которой будет отображаться форма
для загрузки изображений.
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


@app.route('/load_pic/', methods=['GET', 'POST'])
def load_pic():
    if request.method == 'POST':
        result = request.files.get('load-pic-file')
        print(result)
        # return "Файл загружен"
    context = {'title': 'Загрузка картинки'}
    return render_template('load_pic.html', **context)


app.run()
