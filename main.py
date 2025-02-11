import os, re

from skel.routes import ROUTES

# Data that would change in the pages
DYNAMIC_VARIABLES = [
    "name_of_the_page",
    "content_of_the_page"
]

def compile(truncate = False):
    if truncate:
        for files in os.listdir("build"):
            os.remove(f"build/{files}")
    for _file in ROUTES:
        with open(f"build/{_file}.html", 'a') as stream:
            for row in open("skel/html/header.html"):
                stream.write(row)
            stream.write("\n")
            for row in open(f"skel/pages/{_file}.html"):
                stream.write(f"\t\t{row}")
            stream.write("\n")
            for row in open("skel/html/footer.html"):
                stream.write(row)

compile(True)
