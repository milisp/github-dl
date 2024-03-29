# github-file-dl

> download github special files. Resuming interrupted downloads  

> 下载 github 某个文件夹或文件，可以断点续传

## Install

```sh
pip install git+https://github.com/milisp/github-file-dl
```

## Usage

```
positional arguments:
  url                   github folder url or file url

options:
  -h, --help            show this help message and exit
  -p PROXY, --proxy PROXY
                        https_prxoy url
  -d DIR, --dir DIR     special output directory
  --skip-media          skip image video and audio
  --skip-image          skip image
  --skip-audio          skip audio
  --skip-video          skip video
  -v, --verbose
```

## main code file

[`__main__.py`](src/github_file_dl/__main__.py)

## Similar or related Projects

- [github-files-fetcher](https://github.com/Gyumeijie/github-files-fetcher) - nodejs
- [fetch](https://github.com/gruntwork-io/fetch) - golang
