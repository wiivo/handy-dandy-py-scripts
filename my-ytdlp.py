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
                    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('url', metavar="URL", nargs='+',
                    help='youtube url')
parser.add_argument('-a', "--audio", action='store_true', default=False,
                    help='flag to download audio file')
parser.add_argument('-m', "--metadata", action='store_true', default=False,
                    help='flag to embed metadata and thumbnail')
parser.add_argument('-f',"--force-h264", action='store_true', default=False,
                    help='flag to force convert to H.264')
parser.add_argument('-i',"--items", type=str,
                    help="items to download, for example '1:3,7,-5::2' on a playlist of size 15 will download 1,2,3,7,11,13,15")
parser.add_argument('-p', "--path", type=dir_path, default=os.getcwd(),
                    help='set path')
parser.add_argument('-t' ,'--trim', type=timestamp, default=timestamp(), metavar='TIMESTAMP',
                    help='trim download using timestamp, for example:\n-t 0:14-1:23\n-t 0:14')
parser.add_argument('-v','--version', action='version', version='%(prog)s v1.0')

args = parser.parse_args()

ytdlp = ["yt-dlp", *args.url, "-P", args.path, "--format", "bestvideo+bestaudio"]

if args.force_h264:
    if not args.audio:
        ytdlp.extend(["--exec", "ffmpeg -i {} -c:v libx264 -c:a aac -strict -2 {}_AVC.mp4",
         "--exec", "del {}" if sys.platform == "win32" else "rm {}"])
    else:
        ytdlp.extend(["--exec", "ffmpeg -i {} -vn -ar 44100 -ac 2 -b:a 192k {}_AVC.mp3",
         "--exec", "del {}" if sys.platform == "win32" else "rm {}"])

if args.items:
    ytdlp.extend(["-I", args.items])

if args.trim:
    ytdlp.extend(["--download-sections", f"*{args.trim}", "-S", "proto:https"])

if args.audio:
    ytdlp.extend(["--extract-audio", "--audio-format", "mp3", "--audio-quality", "3"])

if args.metadata:
    ytdlp.extend(["--add-metadata", "--embed-thumbnail"])

try:
    run(ytdlp)
except FileNotFoundError:
    print("\033[91mERROR:\033[0m yt-dlp is not installed or added to PATH")