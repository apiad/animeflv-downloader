import requests
import bs4
import re
from tqdm import tqdm
from pathlib import Path
import time
import json
from selenium.webdriver import Firefox, FirefoxOptions


def search_anime(query: str, find_details:bool = True):
    url = f"https://www3.animeflv.net/browse?q={query}"
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, features="html.parser")

    items = soup.find("ul", {'class': 'ListAnimes'}).find_all('li')
    results = {}

    for item in tqdm(items, desc="Looking up details", unit=' title'):
        title = item.find("h3", {'class': 'Title'}).text
        item_url = item.find('a').attrs['href'].replace('/anime/', "")

        if find_details:
            item_html = requests.get(f"https://www3.animeflv.net/anime/{item_url}").text
            anime_details = re.search(r"var episodes = (?P<list_items>\[.+\]);", item_html).groups('list_items')[0]
            total_chapters = eval(anime_details)[0][0]
        else:
            total_chapters = None

        results[title] = (item_url, total_chapters)

    return results


def find_details(anime_id:str):
    item_html = requests.get(f"https://www3.animeflv.net/anime/{anime_id}").text
    anime_details = re.search(r"var episodes = (?P<list_items>\[.+\]);", item_html).groups('list_items')[0]
    description = bs4.BeautifulSoup(item_html, features="html.parser").find("div", {'class': 'Description'}).text
    total_chapters = eval(anime_details)[0][0]

    return total_chapters, description


def download_one(title: str, chapter: int, output_path: str, return_url:bool=False):
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
    options = FirefoxOptions()
    options.headless = True
    driver = Firefox(executable_path=Path(__file__).parent / "geckodriver", options=options)

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

    if return_url:
        return video_url

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
    except:
        path.unlink()
        raise

    return path
