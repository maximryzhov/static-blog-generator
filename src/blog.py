import argparse
import os
import time
import shutil
from distutils.dir_util import copy_tree


def choose_or_exit(message):
    choice = ""
    while choice.lower() not in ("y", "n", "yes", "no"):
        choice = input(message)
        if choice.lower() in ("n", "no"):
            exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['copysettings', 'copystatic', 'build'])
    args = parser.parse_args()

    if args.command == "build":
        from core import build_all

        print("Building pages..")
        start = time.time()
        build_all()
        print(f"Built in {time.time() - start:.2f} seconds")

    elif args.command == 'copysettings':
        base_dir = os.path.dirname(os.path.abspath(__file__))

        if os.path.exists(os.path.join(base_dir, "settings.py")):
            choose_or_exit("File 'settings.py' already exists. Do you wish to overwrite it?")

        src = os.path.join(base_dir, "settings.py.example")
        dest = os.path.join(base_dir, "settings.py")
        shutil.copy(src, dest)
        print(f"Copied settings file to {base_dir}")

    elif args.command == 'copystatic':
        from settings import BASE_DIR, PUBLIC_DIR

        if os.path.exists(PUBLIC_DIR):
            choose_or_exit(f"Folder '{PUBLIC_DIR}' already exists.\nDo you wish to overwrite it?")

        copy_tree(os.path.join(BASE_DIR, "..", "staticfiles"), PUBLIC_DIR)
        print(f"Copied default static files to {PUBLIC_DIR}")
