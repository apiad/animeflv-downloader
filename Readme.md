# AnimeFLV.net downloader

> Check the bot at https://t.me/animeflv_download_bot

This script is very simple, it will attempt to download video files from [AnimeFLV.net](https://animeflv.net).
It also works as Telegram Bot!

> **DISCLAIMER:** This project is for personal and legitimate use ONLY. It is not designed for commercial use. 
> I do not endorse blatanly downloading copyrighted material from anywhere in the Internet.
> That being said, if you are from a Third World country where this content is simply not available, you only have an intermitent or unreliable Internet connection, and the content is only for your personal consumption, that can be considered that a legitimate use.
>
> Please support [AnimeFLV.net](https://animeflv.net) in any way you can. Specially, do visit the website and what the chapters through streaming if you can afford it. They make an awesome job and they deserve your support.

### Install

Just run:

    pip install -r requirements.txt

### Usage

Pass the title of an anime series as it appears in the URL. For example, for <https://www3.animeflv.net/anime/shingeki-no-kyojin> the title is `shingeki-no-kyojin`, and optionally the initial and final episode:

    python -m animeflv download shingeki-no-kyojin 1 25 [--output_path <path>]

If you don't know the exact URL, try `search`:

    python -m animeflv search "shingeki no kyojin"

It will print something like:

    Shingeki no Kyojin: Kuinaki Sentaku [2 chapters] ( shingeki-no-kyojin-kuinaki-sentaku )
    Shingeki no Kyojin Season 2 [12 chapters] ( shingeki-no-kyojin-season-2 )
    Shingeki no Kyojin OVA [3 chapters] ( shingeki-no-kyojin-ova )
    Shingeki no Kyojin Season 3 [12 chapters] ( shingeki-no-kyojin-season-3 )
    Shingeki no Kyojin Live Action [1 chapters] ( shingeki-no-kyojin-live-action )
    Shingeki no Kyojin Movie 1: Guren no Yumiya [1 chapters] ( shingeki-no-kyojin-movie-1-guren-no-yumiya )
    Shingeki no Kyojin Movie 2: Jiyuu no Tsubasa [1 chapters] ( shingeki-no-kyojin-movie-2-jiyuu-no-tsubasa )
    Shingeki no Kyojin [25 chapters] ( shingeki-no-kyojin )
    Shingeki no Kyojin: Chimi Kyara Gekijou - Tondeke! Kunren Heidan [9 chapters] ( shingeki-no-kyojin-chimi-kyara-gekijou-tondeke )
    Shingeki no Kyojin Season 3 Part 2 [10 chapters] ( shingeki-no-kyojin-season-3-part-2 )
    Shingeki no Kyojin: Lost Girls [3 chapters] ( shingeki-no-kyojin-lost-girls )

After seeing the search results, if you want to simply download **all chapters** from **all the listed anime**, just type:

    python -m animeflv search <query> --download_all

> WARNING: This option can download A LOT of episodes sometimes. Use with care.

### Telegram Bot

If you want to run the Telegram bot (you should know what you're doing):

    python -m animeflv.bot <TOKEN>

The bot requires `MP4Box` installed, in Debian-based distributions (Ubuntu) this app is the `gpac` package:

    apt install gpac

### Docker

If you prefer docker, running the bot it is even easier:

    TOKEN=<your-token> docker-compose up

## How does it work?

It's kind of tricky, because videos are embedded, hence we require:

1. Download the webpage from <animeflv.net> that contains the link to the embedded video.
2. Parse the HTML, find a `script` tag that contains a variable called `videos` which contains a dictionary with all links.
3. Search for the link that points to GoCDN.
4. Now it becomes tricky, because GoCDN doesn't actually host the video, but embeds it from another URL. The thing is, you have to click the play button for a script to execute that will inject the video player with the actual url. Hence, at this point we open a Firefox browser (using `selenium`) and automatically click that button, steal the url, and then proceed to download.

## Will this work reliably?

I doubt it. If something fails, i.e., there is no GoCDN link for that specific show, or the HTML layout changes, or the way the whole hosting works changes, this will break. It works for now as far as I've tried, but collaboration is always accepted to improve reliability.

## License and Collaboration

MIT, so... you know the drill. Fork, pull-request, rinse and repeat.
