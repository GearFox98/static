# This file has the function definitions for the tool
# to work, don't mess here unless you know what you're
# doing!

import os
from typing import Iterable
import routes

TEMP = "build/{0}.html"
HTML = "html/{0}.html"

# Checks directories in order to perform validation before building the site
def check_dirs() -> bool:
    DIRS = ('build', 'dist', 'html', 'pages')
    error = False
    for d in DIRS:
        if not os.path.exists(d):
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

# Build each page in a temporary folder, it is called in 'routes' script
def build_content(pages: Iterable[str], content: Iterable[str]):
    for page in pages:
        index = 0
        with open(f"build/{page}", 'w') as document:
            document.writelines(content[0].split("\n"))
        index += 1

# Compile the whole site into dist folder
def compile() -> bool:
    for files in os.listdir("build"):
        os.remove(f"build/{files}")
    
    for _file in routes.ROUTES:
        with open(f"dist/{_file}.html", 'a') as stream:
            for row in open(HTML.format("header")):
                stream.write(row)
            stream.write("\n")
            
            for row in open(TEMP.format(_file)):
                stream.write(f"{row}")
            stream.write("\n")
            
            for row in open(HTML.format("footer")):
                stream.write(row)
    return False

def build_site():
    print("Checking directories...")
    error = check_dirs()
    if error:
        print("Please, set up your files before building the site!")
        return
    else:
        print("Building temporary files...")
        routes.build()
        print("Building site...")
        error = compile()
        if error:
            print("There were some errors...")
        else:
            print("Site built successfully, check the 'dist' folder")