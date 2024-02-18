from flask import Flask, render_template, request, flash, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = b'94dc38deee56cf4e4e64530d5c9d09f3e6295e7ee7c3811eb8c2c88f8d76b0db'


@app.route('/')
def index():
    context = {
        'title': 'Вход',
        'name': 'Voldemort'
    }
    response = make_response(render_template('main.html', **context))
    response.headers['new_head'] = 'New-value'
    response.set_cookie('username', context['name'])
    # return render_template('index.html', **context)
    return response


@app.route('/getcookie/')
def get_cookies():
    # получаем значение cookie
    name = request.cookies.get('username')
    return f"Значение cookie: {name}"


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
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('form'))
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('form'))
    return render_template('flash_form.html')


if __name__ == '__main__':
    app.run(debug=True)
