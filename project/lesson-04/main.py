'''
Задание №1
- Написать программу, которая считывает список из 10 URL-адресов
 и одновременно загружает данные с каждого адреса.
- После загрузки данных нужно записать их в отдельные файлы.
- Используйте потоки.
'''

'''
Задание №2
� Написать программу, которая считывает список из 10 UR-Lадресов 
и одновременно загружает данные с каждого адреса.
� После загрузки данных нужно записать их в отдельные
файлы.
� Используйте процессы.
'''

import threading
import time
import os
import requests
import asyncio
import aiohttp
from multiprocessing import Process


async def download_async(url, start_time):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = 'asyncio_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
            with open(os.path.join('./download/', filename), "w", encoding='utf-8') as f:
                f.write(text)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


def download(url, start_time):
    response = requests.get(url)
    filename = 'multiprocessing_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(os.path.join('./download/', filename), "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


def task1(urls):
    threads = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=download, args=[url, start_time])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def task2(urls):
    processes = []
    start_time = time.time()
    for url in urls:
        process = Process(target=download, args=(url, start_time))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()


async def task3(urls, start_time):
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_async(url, start_time))
        tasks.append(task)
    await asyncio.gather(*tasks)


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
    start_time = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(task3(urls, start_time))


if __name__ == '__main__':
    main()
