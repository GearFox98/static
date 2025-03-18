#!/usr/bin/env python3

import os, sys, shutil, time
from lxml import etree, html
from static_lib.stutils import (
    exists,
    clear
    )
from static_lib import registry
from routes import build, ROUTES, HTML, BUILD_DIR

# Checks directories in order to perform validation before building the site
def check_dirs() -> bool:
    DIRS = ('build', 'dist', 'html', 'pages', 'data')
    error = False
    for d in DIRS:
        if not exists(d):
            os.mkdir(d)
            match d:
                case 'html':
                    print("Warning: html directory is empty, make sure to provide a 'header.html' and 'footer.html' file")
                    error = True
                case 'pages':
                    print("Info: the pages directory is empty, define some pages and link them in the 'routes.py' script")
                    error = True
                case _:
                    print(f"Folder: {d} was created successfully")
    return error

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

# Compile the whole site into dist folder
def compile() -> bool:
    # Clean dist files
    for files in os.listdir("dist"):
        clear(f"dist/{files}")

    for _file in ROUTES:
        with open(f"dist/{_file}", 'a') as stream:
            for row in open(HTML.format("header")):
                stream.write(row)

            for row in open(BUILD_DIR.format(_file)):
                stream.write(f"{row}")

            for row in open(HTML.format("footer")):
                stream.write(row)
        prettify(f"dist/{_file}", f"dist/{_file}.html")
        os.remove(f"dist/{_file}")
    return False

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

def site_build() -> bool:
    print("Checking dirs...")
    check_dirs()
    print("Building temporary files...")
    build()
    if not compile():
        copy_data()
        return True
    else:
        return False

def watch():
    while True:
        tstamp = registry.Timestamp(".")
        tstamp.update_times()

        if tstamp.compare_times():
            print("Rebuilding...")
            build()
            if not compile():
                copy_data()
                print("Press F5 in your browser")
            else:
                print("Something went wrong")
        
        time.sleep(5)

if __name__ == "__main__":
    success = site_build()
    if success:
        print("Done")
    else:
        print("There were some errors")
    sys.exit(0)