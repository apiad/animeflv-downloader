# coding: utf-8

from prompt_toolkit import output
from .api import search_anime, download_one
import fire


def download(title: str, start: int = 1, end: int = 1, output_path: str = ".", override:bool = False):
    for chapter in range(start, end + 1):
        download_one(title, chapter=chapter, output_path=output_path, override=override)


def search(query: str, download_all: bool = False, output_path: str = ".", override:bool = False):
    results = search_anime(query)

    for title, (url, chapters) in results.items():
        print(title, f"[{chapters} chapters]", f"( {url} )")

    if download_all:
        for title, (url, chapters) in results.items():
            download(url, start=1, end=chapters, output_path=output_path, override=override)


if __name__ == "__main__":
    fire.Fire(dict(
        download=download,
        search=search,
    ))
