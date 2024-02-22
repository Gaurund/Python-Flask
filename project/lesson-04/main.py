'''
Задание №1
- Написать программу, которая считывает список из 10 URL-адресов
 и одновременно загружает данные с каждого адреса.
- После загрузки данных нужно записать их в отдельные файлы.
- Используйте потоки.
'''


import time
import os
import requests


def download(url, start_time):
    response = requests.get(url)
    filename = 'sync_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(os.path.join('./download/', filename), "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


def task1(urls):
    start_time = time.time()
    for url in urls:
        download(url, start_time)


def main():
    urls = ['https://www.google.ru/',
            'https://gb.ru/',
            'https://ya.ru/',
            'https://www.python.org/',
            'https://habr.com/ru/all/',
            'https://mail.ru/',
            'https://www.yahoo.com/',
            'https://www.rambler.ru/',
            'https://ru.wikipedia.org/',
            'https://pikabu.ru/'
            ]

    task1(urls)


if __name__ == '__main__':
    main()
