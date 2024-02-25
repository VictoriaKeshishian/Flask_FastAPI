# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию
# изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем
# времени выполнения программы.

import requests
import os
import concurrent.futures
import asyncio
import aiohttp
import time
import sys


# Функция для скачивания изображения и сохранения его на диск
def download_image(url):
    filename = url.split('/')[-1]
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename


# Функция для асинхронного скачивания изображения и сохранения его на диск
async def async_download_image(session, url):
    filename = url.split('/')[-1]
    async with session.get(url) as response:
        with open(filename, 'wb') as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
    return filename


# Функция для многопоточного и многопроцессорного скачивания изображений
def download_images_multithreaded(urls):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(download_image, url))
        for future in concurrent.futures.as_completed(futures):
            try:
                filename = future.result()
                print(f"Изображение {filename} загружено. Время: {time.time() - start_time}")
            except Exception as e:
                print(f"Ошибка: {e}")
    print(f"Общее время выполнения: {time.time() - start_time} секунд")


# Функция для асинхронного скачивания изображений
async def download_images_async(urls):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(async_download_image(session, url)))
        await asyncio.gather(*tasks)
    print(f"Общее время выполнения: {time.time() - start_time} секунд")

# Получаем список URL-адресов из аргументов командной строки
urls = sys.argv[1:]

# Проверяем, были ли переданы URL-адреса
if not urls:
    print("Пожалуйста, укажите хотя бы один URL-адрес.")
    sys.exit(1)

# Многопоточное и многопроцессорное скачивание изображений
print("Многопоточное и многопроцессорное скачивание:")
download_images_multithreaded(urls)

# Асинхронное скачивание изображений
print("\nАсинхронное скачивание:")
asyncio.run(download_images_async(urls))


# команда для запуска:
#  python Home_work/Hw_4/asyncio_01.py https://funik.ru/wp-content/uploads/2018/10/17478da42271207e1d86.jpg
# загруженный файл в корневом каталоге