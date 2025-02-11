import os, re

from skel.routes import ROUTES
from lib.parser import parse

# Variable line format!
VARIABLE_FORMAT = re.compile("^[A-Za-z0-9_]+=\"$")

# Data that would change in the pages
DYNAMIC_VARIABLES = [
    "name_of_the_page",
    "content_of_the_page"
]

PAGES = "skel/pages/{0}.html"
HTML = "skel/html/{0}.html"

def set_build_directory():
    if not os.path.exists("build"):
        os.mkdir("build")

parse(PAGES, "index")

def compile(truncate = False):
    set_build_directory()

    if truncate:
        for files in os.listdir("build"):
            os.remove(f"build/{files}")
    
    for _file in ROUTES:
        with open(f"build/{_file}.html", 'a') as stream:
            for row in open(HTML.format("header")):
                stream.write(row)
            stream.write("\n")
            
            for row in open(PAGES.format(_file)):
                stream.write(f"{row}")
            stream.write("\n")
            
            for row in open(HTML.format("footer")):
                stream.write(row)

#compile(True)
