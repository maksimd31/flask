from urllib.request import urlopen, urlretrieve
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
import aiohttp
import time
import argparse


def download_image(url: str) -> str:
    """Download an image from a given url and save it to disk"""
    filename = url.split("/")[-1]
    with urlopen(url) as img, open(filename, "wb") as f:
        f.write(img.read())
    return filename


def download_with_threads(urls: list) -> list:
    """Download images with threads"""
    results = []
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        futures = [executor.submit(download_image, url) for url in urls]
        for future in futures:
            result = future.result()
            results.append(result)
    return results


def download_with_processes(urls: list) -> list:
    """Download images with processes"""
    results = []
    with ProcessPoolExecutor(max_workers=len(urls)) as executor:
        futures = [executor.submit(download_image, url) for url in urls]
        for future in futures:
            result = future.result()
            results.append(result)
    return results


async def download_image_async(session: aiohttp.ClientSession, url: str) -> str:
    """Download an image asynchronously"""
    filename = url.split("/")[-1]
    async with session.get(url) as response:
        async with open(filename, "wb") as f:
            f.write(await response.content.read())
    return filename


async def download_with_async(urls: list) -> list:
    """Download images asynchronously"""
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, url) for url in urls]
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download images from urls.')
    parser.add_argument('urls', metavar='url', nargs='+', help='an URL to download an image from')
    args = parser.parse_args()

    print("Downloading images with threads...")
    start_time = time.time()
    download_with_threads(args.urls)
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

    print("Downloading images with processes...")
    start_time = time.time()
    download_with_processes(args.urls)
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

    print("Downloading images asynchronously...")
    start_time = time.time()
    asyncio.run(download_with_async(args.urls))
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
