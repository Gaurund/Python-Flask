from flask import Flask, render_template

'''
Задание

Создать базовый шаблон для интернет-магазина, 
содержащий общие элементы дизайна (шапка, меню, подвал), 
и дочерние шаблоны для страниц категорий товаров 
и отдельных товаров. 
Например, создать страницы «Одежда», «Обувь» и «Куртка», 
используя базовый шаблон.
'''

shop = Flask(__name__)


@shop.route('/')
def index():
    return render_template('base.html')


@shop.route('/clothes/')
def clothes():
    clothes = [{'name': 'Куртка, мужская', 'pic_url': '/static/img/02898312_2_500.jpg', 'annotation': 'Черная мужская куртка', 'price': 12500},
               {'name': 'Куртка, женская', 'pic_url': '/static/img/3450518118_60_4.jpg',
                'annotation': 'Женская куртка, белая', 'price': 99500},
               {'name': 'Детская куртка', 'pic_url': '/static/img/2796570219.jpg',
                'annotation': 'Детская жёлтая куртка', 'price': 5500}

               ]
    return render_template('clothes.html', context=clothes)


@shop.route('/shoes/')
def shoes():
    shoes = [{'name': 'Туфли мужские', 'pic_url': '/static/img/1.webp',
              'annotation': 'Коричневые с жёлтой подошвой', 'price': 9500},
               {'name': 'Туфли мужские', 'pic_url': '/static/img/2.jpg',
                'annotation': 'Полностью коричневые', 'price': 10500},
               {'name': 'Туфли мужские', 'pic_url': '/static/img/3.jpg',
                'annotation': 'На самом деле те же самое что и выше.', 'price': 10500},
             {'name': 'Туфли мужские', 'pic_url': '/static/img/4.jpg',
              'annotation': 'Светло-коричныевые с чёрной подошвой', 'price': 7990}

               ]
    return render_template('shoes.html', context=shoes)


if __name__ == '__main__':
    shop.run()
