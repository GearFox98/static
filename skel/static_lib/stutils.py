import os, shutil, time
from typing import Iterable

# region path
def exists(path: str) -> bool:
    return os.path.exists(path)

def is_empty(path: str) -> bool:
    return False if len(os.listdir(path)) == 0 else True

# Build each page in a temporary folder, it is called in 'routes' script
def build_content(pages: Iterable[str], content: Iterable[str]):
    for i in range(len(pages)):
        with open(f"build/{pages[i]}.html", 'w') as document:
            document.writelines(content[i])

# Media refactor
def media(res: str):
    return f"\"data/{res}\""

# Clear paths
def clear(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
# endregion

# region server_related

def print_shutdown():
    print("\rShutting down.", end="")
    time.sleep(0.2)
    print("\rShutting down..", end="")
    time.sleep(0.2)
    print("\rShutting down...", end="")
    time.sleep(0.2)

# endregion