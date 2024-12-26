#!/usr/bin/env python
import argparse, os
from subprocess import run

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

parser = argparse.ArgumentParser(
                    prog='my-ytdlp',
                    description='Custom simplified ytdlp script',
                    usage="my-ytdlp URL [-a] [-d DIR]"
)

parser.add_argument('url', metavar="URL", nargs='+',
                    help='youtube url')
parser.add_argument('-a', "--mp3", action='store_true', default=False,
                    help='flag to download audio file.')
parser.add_argument('-d', "--dir", type=dir_path, default=os.getcwd(),
                    help='set directory')
parser.add_argument('-v','--version', action='version', version='%(prog)s v1.0')

args = parser.parse_args()

ytdlp = ["yt-dlp", *args.url, "--add-metadata", "-P", args.dir]
if args.mp3:
    ytdlp.extend(["--extract-audio", "--audio-format", "mp3", "--audio-quality", "3", "--embed-thumbnail"])
else:
    ytdlp.extend(["--format", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"])

try:
    run(ytdlp)
except FileNotFoundError:
    print("\033[91mERROR:\033[0m yt-dlp is not installed or added to PATH")