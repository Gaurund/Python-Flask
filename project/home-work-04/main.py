'''
Задание

Написать программу, которая скачивает изображения с заданных URL-адресов
и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле,
название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес:
 https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный,
  многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов
  через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени
  скачивания каждого изображения и общем времени выполнения программы.
'''

import argparse
import asyncio
import os
import threading
import time
import aiohttp
import requests
from multiprocessing import Process


def cut_name(url):
    filename = url.split('/')
    return filename[-1]


def download_file(url):
    response = requests.get(url)
    filename = cut_name(url)
    start_time = time.time()
    with open(os.path.join('./download/', filename), "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} in {time.time() - start_time:.6f} seconds")


async def download_file_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            file = await response.read()
            filename = cut_name(url)
            start_time = time.time()
            with open(os.path.join('./download/', filename), "wb") as f:
                f.write(file)
            print(f"Downloaded {url} in {time.time() - start_time:.6f} seconds")


def download_list_of_files(urls):
    for file in urls:
        download_file(file)


def download_threads(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_file, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def download_processes(urls):
    processes = []
    for url in urls:
        process = Process(target=download_file, args=[url])
        processes.append(process)
        process.start()
    for process in processes:
        process.join()


async def download_async(urls):
    files = []
    for url in urls:
        task = asyncio.ensure_future(download_file_async(url))
        files.append(task)
    await asyncio.gather(*files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='FileDownloader',
        description='''The program takes in URL strings and requests those files. 
        Use --mode key to define (a)synchronous or (p)rocesses or (t)hreading method.'''
    )
    parser.add_argument('line', type=str, nargs='*', help="Input an URL address(es)")
    parser.add_argument('-m', '--method', type=str, nargs=1,
                        help="Choose a method: (a)synchronous or (p)rocesses or (t)hreading.")
    args = parser.parse_args()
    start_time = time.time()
    if args.method:
        if args.method[0] == 't':
            print('Use threads:')
            download_threads(args.line)
        elif args.method[0] == 'p':
            print('Use processes:')
            download_processes(args.line)
        elif args.method[0] == 'a':
            print('Use asynchronous:')
            asyncio.run(download_async(args.line))
    else:
        print('Do it like old-timers:')
        download_list_of_files(args.line)
    print(f'It took {time.time() - start_time:.6f} seconds to download the file(s).')
