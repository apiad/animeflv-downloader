# coding: utf-8

from tqdm import tqdm
from selenium.webdriver import Firefox
import requests
import bs4
import json
import time
import fire
from pathlib import Path


def main(title: str, start: int = 1, end: int = 1, output_path: str = "."):
    for chapter in range(start, end + 1):
        download(title, chapter, output_path)


def download(title: str, chapter: int, output_path: str):
    print("Downloading AnimeFLV.net webpage")
    html = requests.get(f"https://www3.animeflv.net/ver/{title}-{chapter}").text

    print("Looking for GoCDN link")

    soup = bs4.BeautifulSoup(html, features="html.parser")
    lines = str(soup).split("\n")

    for l in lines:
        if l.strip().startswith("var videos = {"):
            break

    l = l.strip()
    data = json.loads(l[13:-1])
    for d in data["SUB"]:
        if d["server"] == "gocdn":
            break

    url = d["code"]

    print("Found GoCDN url")
    print(url)

    print("Opening Firefox (for later...)")
    driver = Firefox(executable_path=Path(__file__).parent / "geckodriver")
    driver.minimize_window()

    print("Getting the URL")
    driver.get(url)

    print("Clicking the play button")
    play = driver.find_element_by_css_selector("img#start")
    play.click()

    time.sleep(3)

    video_obj = driver.find_element_by_css_selector("video.jw-video")
    video_url = video_obj.get_attribute("src")

    print("Found video link")
    print(video_url)
    driver.close()

    print("Downloading video")
    
    stream = requests.get(video_url, stream=True)
    total_size = int(stream.headers.get('content-length', 0))
    path = Path(output_path) / f"{title}-{chapter}.mp4"

    if path.exists():
        print(f"(!) Overwriting {path}")

    try:
        with path.open("wb") as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for data in stream.iter_content(32*1024):
                    f.write(data)
                    pbar.update(len(data))

        return True
    except:
        path.unlink()
        raise


if __name__ == "__main__":
    fire.Fire(main)
