import os, shutil
from typing import Iterable
from lxml import etree, html

# Prettify HTML code
def prettify(src: str, dest: str):
    source = open(src, "r")

    _html = ""
    for line in source.readlines():
        _html = _html + line.strip(" ").strip("\t").strip("\n").strip(" ").strip("\t")
    document_root = html.fromstring(_html)
    pretty = etree.tostring(document_root, encoding='unicode', pretty_print=True)

    source.close()

    with open(dest, "a") as destiny:
        destiny.write("<!DOCTYPE html>\n")
        for line in pretty:
            destiny.write(line)

def exists(path: str) -> bool:
    return os.path.exists(path)

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

# Copy static data into dist folder
def copy_data():
    SRC = "data"
    DEST = "dist/data"
    if exists(DEST):
        source = os.listdir(SRC)
        destination = os.listdir(DEST)
        for obj in source:
            if not obj in destination:
                shutil.copytree(SRC, DEST, dirs_exist_ok=True)
    else:
        shutil.copytree(SRC, DEST, dirs_exist_ok=True)
