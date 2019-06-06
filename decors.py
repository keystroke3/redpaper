import requests
import time
import functools
import logging

url = "http://getwallpapers.com/wallpaper/full/4/c/3/977216-free-download-ariana-grande-wallpapers-1920x1200-smartphone.jpg"
headers = {'user-agent': 'Mozila/5.0'}


def event_log():
    

def timer(func):
    @functools.wraps(func)
    def timer_wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        stop = time.perf_counter()
        func_time = stop-start
        print(f"{func.__name__} executed in {func_time:.4f}")
        return value
    return timer_wrapper


@timer
def stream_download():
    r = requests.get(url=url, headers=headers, stream=True)

    with open("ariana_stream.jpg", 'wb') as img:
        for chunk in r.iter_content(chunk_size=128):
                img.write(chunk)


@timer
def get_download():
    r = requests.get(url=url, headers=headers)
    with open("ariana_get.jpg", 'wb') as img:
        for chunk in r.iter_content(chunk_size=128):
                img.write(chunk)

