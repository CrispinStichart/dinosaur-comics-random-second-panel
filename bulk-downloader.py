#!/bin/env python

from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import threading
from pathlib import Path
import os

URL = "https://qwantz.com/index.php"
BASE_URL = "https://qwantz.com/"
SECOND_PANEL_DIR = "panels/"

# left, upper, right, lower
CROP_AREA = (246, 2, 372, 241)


class NoMoreComics(Exception):
    pass


class AtomicCounter:
    def __init__(self, start=0):
        self.value = start
        self.lock = threading.Lock()

    def inc(self, increment=1):
        with self.lock:
            self.value += increment

    def dec(self, decrement=1):
        with self.lock:
            self.value -= decrement

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


def get_html(comic_num: int) -> BeautifulSoup:
    payload = {"comic": comic_num}
    r = requests.get(URL, params=payload, allow_redirects=False)
    if r.status_code != 200:
        # When the requested comic doesn't exist, the page redirects to
        # the base url (qwantz.com).
        print(f"No comic for number {comic_num}!")
        raise NoMoreComics

    return BeautifulSoup(r.text, "html.parser")


def extract_comic_url(soup: BeautifulSoup) -> str:
    # relative URL
    comic_url = soup.find(class_="comic")["src"]
    return BASE_URL + comic_url


def download_and_crop_comic(url: str, comic_num: int) -> None:
    img = requests.get(url)
    img = Image.open(BytesIO(img.content))
    img = img.crop(CROP_AREA)
    img.save(SECOND_PANEL_DIR + str(comic_num) + ".png")


def download_comic(
    comic_num: int, pool_sema: threading.BoundedSemaphore, missing: AtomicCounter
) -> None:
    with pool_sema:
        try:
            soup = get_html(comic_num)
        except NoMoreComics:
            missing.inc()
            return

        url = extract_comic_url(soup)
        download_and_crop_comic(url, comic_num)

        print(f"Saved comic #{comic_num}")


def already_downloaded(comic_num: int) -> bool:
    filename = SECOND_PANEL_DIR + str(comic_num) + ".png"
    return Path(filename).is_file()


def main():
    try:
        os.mkdir(SECOND_PANEL_DIR)
    except FileExistsError:
        pass

    pool_sema = threading.BoundedSemaphore(value=8)
    # Since there are some random gaps in the comic numbering,
    # we want to allow a reasonable number before deciding that we're done.
    # More intelligent way would be to wait for a sequence of numbers.
    # As of May 2022, when the latest comic was #3893, these were the missing comics:
    # 89, 215, 228, 287, 288, 660, 1373, 1374, 1375, 1376, 1377, 1378, 1487, 1488, 1631
    missing_comics = AtomicCounter()
    i = 1
    while missing_comics.value < 20:
        if not already_downloaded(i):
            # We get a lock here because otherwise we might fire up thousands of threads.
            with pool_sema:
                t = threading.Thread(
                    target=download_comic, args=(i, pool_sema, missing_comics)
                )
                t.start()

        i += 1


if __name__ == "__main__":
    main()
