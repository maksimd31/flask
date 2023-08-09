# Задание
# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.

import requests
import os
import time
import concurrent.futures
from multiprocessing import Pool
from aiohttp import ClientSession
import asyncio
import argparse


def download_images_thread(url):
    filename = os.path.basename(url)
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


def download_images_process(url):
    filename = os.path.basename(url)
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


def download_images_async(url, session):
    filename = os.path.basename(url)
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


async def download_image(url, session):
    filename = os.path.basename(url)
    async with session.get(url) as response:
        with open(filename, 'wb') as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)


async def download_images_asyncio(urls):
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(download_image(url, session)))
        await asyncio.gather(*tasks)


def download_images(urls, async_type):
    if async_type == 'thread':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(download_images_thread, urls)
    elif async_type == 'process':
        with Pool() as pool:
            pool.map(download_images_process, urls)
    elif async_type == 'async':
        asyncio.run(download_images_asyncio(urls))


def main():
    parser = argparse.ArgumentParser(description='Download images from URLs')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='list of URLs to download images from')
    parser.add_argument('--async', dest='async_type', default='thread',
                        choices=['thread', 'process', 'async'], help='async type (thread, process, async)')
    args = parser.parse_args()
    urls = args.urls
    async_type = args.async_type

    start_time = time.perf_counter()

    download_images(urls, async_type)

    end_time = time.perf_counter()

    total_time = end_time - start_time
    print(f'Total time taken: {total_time:.2f} seconds')


if __name__ == '__main__':
    main()
