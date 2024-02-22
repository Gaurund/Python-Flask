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
import os
import time
import requests


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


def download_list_of_files(urls):
    for file in urls:
        download_file(file)


def print_line(messages):
    for message in messages:
        print(f'Строка: {message} ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='FileDownloader',
        description='The program take in URL strings and request this files.'
    )
    # parser.add_argument('-m', '--mode', type=str, nargs=1, help="Выберите режим.")
    parser.add_argument('line', type=str, nargs='*', help="Введите строку.")
    args = parser.parse_args()
    # print(args.mode)
    # if args.mode[0] == 'a':
    #     print('Успех')
    # else:
    #     print('Nope!')
    download_list_of_files(args.line)
    # download_file(args.line[0])
    # cut_name(args.line[0])
