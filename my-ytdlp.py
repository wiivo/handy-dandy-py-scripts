#!/usr/bin/env python
import argparse, os, sys
from subprocess import run

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

def timestamp(value=None):
    if value is None:
        return None

    tokens = value.split("-")
    if len(tokens) == 1 or tokens[1]=="":
        return f"{tokens[0]}-inf"
    elif len(tokens) == 2:
        return value

    raise ValueError()

# hack to allow a leading dash for timestamp
for i in range(len(sys.argv)):
    if sys.argv[i] == '-t' or sys.argv[i] == '--trim':
        if sys.argv[i+1][0] == '-':
            tmp = sys.argv[i+1]
            sys.argv[i+1] = "0:00" + tmp

parser = argparse.ArgumentParser(
                    prog='my-ytdlp',
                    description='Custom simplified ytdlp script',
                    usage="my-ytdlp URL [-a] [-p PATH] [-t TIMESTAMP]",
                    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('url', metavar="URL", nargs='+',
                    help='youtube url')
parser.add_argument('-a', "--mp3", action='store_true', default=False,
                    help='flag to download audio file')
parser.add_argument('-p', "--path", type=dir_path, default=os.getcwd(),
                    help='set path')
parser.add_argument('-t' ,'--trim', type=timestamp, default=timestamp(), metavar='TIMESTAMP',
                    help='trim download using timestamp, for example:\n-t 0:14-1:23\n-t 0:14')
parser.add_argument('-v','--version', action='version', version='%(prog)s v1.0')

args = parser.parse_args()

ytdlp = ["yt-dlp", *args.url, "--add-metadata", "-P", args.path, "--format", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"]

if args.trim:
    ytdlp.extend(["--download-sections", f"*{args.trim}", "-S", "proto:https"])

if args.mp3:
    ytdlp.extend(["--extract-audio", "--audio-format", "mp3", "--audio-quality", "3", "--embed-thumbnail"])

try:
    run(ytdlp)
except FileNotFoundError:
    print("\033[91mERROR:\033[0m yt-dlp is not installed or added to PATH")