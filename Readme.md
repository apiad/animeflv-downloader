# AnimeFLV.net downloader

> Check the bot at https://t.me/animeflv_download_bot

This script is very simple, it will attempt to download video files from <animeflv.net>.
It also works as Telegram Bot!

### Install

Just run:

    pip install -r requirements.txt

### Usage

Pass the title of an anime series as it appears in the <animeflv.net> URL. For example, for <https://www3.animeflv.net/anime/shingeki-no-kyojin> the title is `shingeki-no-kyojin`, and optionally the initial and final episode:

    python -m animeflv download shingeki-no-kyojin 1 25 [--output_path <path>]

If you don't know the exact URL, try `search`:

    python -m animeflv search shingeki

If you want to run the Telegram bot (you should know what you're doing):

    python -m animeflv.bot <TOKEN>

The bot requires `MP4Box` installed, in Debian-based distributions (Ubuntu) this app is the `gpac` package:

    apt install gpac

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