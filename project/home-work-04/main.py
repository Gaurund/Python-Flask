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


def download_file(url):
    pass


def download_list_of_files(urls):
    pass


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
    print_line(args.line)
