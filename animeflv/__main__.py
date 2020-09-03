# coding: utf-8

from .api import search_anime, download_one
import fire


def download(title: str, start: int = 1, end: int = 1, output_path: str = "."):
    for chapter in range(start, end + 1):
        download_one(title, chapter, output_path)


def search(query: str):
    for title, (url, chapters) in search_anime(query).items():
        print(title, f"[{chapters} chapters]", f"( {url} )")


if __name__ == "__main__":
    fire.Fire(dict(
        download=download,
        search=search,
    ))
