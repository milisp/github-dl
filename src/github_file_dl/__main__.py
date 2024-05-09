# coding: utf-8
import argparse
from pathlib import Path

import requests


AUDIO = "mp3 aac"
VIDEO = "mp4 avi mov"
IMAGE = "jpeg jpg png"


def url_to_api(url: str):
    if url.startswith("https://api"):
        return url
    try:
        us = url.split("/")
        new_url = f'https://api.{us[2]}/repos/{us[3]}/{us[4]}/contents/{"/".join(us[7:])}?ref={us[6]}'
        print(new_url)
        return new_url
    except Exception as e:
        print(e, "\nwrong url.")
        exit(1)


def download_file(url, file_name, proxy="", _dir=""):
    if not _dir:
        _dir = "."
    if proxy:
        proxies = {"https_proxy": proxy}
    else:
        proxies = None
    with requests.get(url, stream=True, proxies=proxies, timeout=10) as response:
        file_path = Path(_dir) / file_name
        parent_path = file_path.parent
        if not parent_path.exists():
            parent_path.mkdir(parents=True)
        with open(file_path, "ab") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


def vprint(args, *s):
    if args.verbose:
        print(*s)


def dl(source_url, args):
    url = url_to_api(source_url)
    if args.proxy:
        proxies = {"https_proxy": args.proxy}
    else:
        proxies = None
    r = requests.get(url, proxies=proxies)
    data = r.json()
    if isinstance(data, dict):
        download_file(data["download_url"], data["path"], args.proxy, args.dir)
    elif isinstance(data, list):
        for p in data:
            durl = p["download_url"]
            vprint(args, durl)
            if durl:
                extension = p["path"].rsplit(".")[-1].lower()
                path = Path(p["path"])
                if args.skip_audio:
                    if extension in AUDIO:
                        continue
                if args.skip_image:
                    if extension in IMAGE:
                        continue
                if args.skip_video:
                    if extension in VIDEO:
                        continue
                if args.skip_media:
                    if extension in f"{AUDIO} {IMAGE} {VIDEO}":
                        continue
                vprint(args, "dl", path)
                if not path.exists() or p["size"] != path.stat().st_size:
                    download_file(durl, path, args.proxy, args.dir)
            else:
                vprint(args, p["html_url"])
                dl(p["html_url"], args)
    else:
        print("data", data)


def main():
    parser = argparse.ArgumentParser(
        prog="github-file-dl",
        description="download github folder or file",
    )
    parser.add_argument("url", help="github folder url or file")
    parser.add_argument("-p", "--proxy", help="https_prxoy url")
    parser.add_argument("-d", "--dir", help="special output directory")
    parser.add_argument(
        "--skip-media", action="store_true", help="skip image video and audio"
    )  # on/off flag
    parser.add_argument("--skip-image", action="store_true", help="skip image")
    parser.add_argument("--skip-audio", action="store_true", help="skip audio")
    parser.add_argument("--skip-video", action="store_true", help="skip video")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    print(args.url, args)
    dl(url_to_api(args.url), args)


if __name__ == "__main__":
    main()
