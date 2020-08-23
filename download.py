# coding: utf-8

from selenium.webdriver import Firefox
import requests
import bs4
import json
import time
import fire


def main(title: str, start: int = 1, end: int = 1):
    for chapter in range(start, end + 1):
        download(title, chapter)


def download(title: str, chapter: int):
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
    driver = Firefox(executable_path="./geckodriver")

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

    with open(f"{title}-{chapter}.mp4", "wb") as fp:
        for batch in requests.get(video_url, stream=True).iter_content(
            chunk_size=32 * 1024
        ):
            fp.write(batch)


if __name__ == "__main__":
    fire.Fire(main)
