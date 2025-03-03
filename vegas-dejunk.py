import os, re, argparse

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

parser = argparse.ArgumentParser(
                    prog='vegas-dejunk',
                    description='Delete sfk files of nonexisting (or all) videos in a directory',
                    usage="vegas-dejunk [-p PATH] [-d]"
)

parser.add_argument('-d', "--dry", action='store_true', default=False,
                    help='do a dry run')
parser.add_argument('-a', "--all", action='store_true', default=False,
                    help='delete all sfk files, not just of nonexisting videos')
parser.add_argument('-p', "--path", type=dir_path, default=os.getcwd(),
                    help='set path')
parser.add_argument('-v','--version', action='version', version='%(prog)s v1.0')

args = parser.parse_args()

dir_list = os.listdir(args.path)

for file in dir_list:
    file_path = os.path.join(args.path, file)
    if os.path.isfile(file_path) and re.search(r'\.sfk\d?$', file) and (file[:-5] not in dir_list or args.all):
        if (args.dry == False):
            os.remove(file_path)
        print(file + " deleted")

print("All clear!")
