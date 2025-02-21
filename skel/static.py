# This file has the function definitions for the tool
# to work, don't mess here unless you know what you're
# doing!

import os
from routes import (
    build,
    ROUTES,
    HTML,
    BUILD_DIR
    )

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

# Compile the whole site into dist folder
def compile() -> bool:
    # Clean dist files
    for files in os.listdir("dist"):
        os.remove(f"dist/{files}")
    
    for _file in ROUTES:
        with open(f"dist/{_file}.html", 'a') as stream:
            for row in open(HTML.format("header")):
                stream.write(row)
            
            for row in open(BUILD_DIR.format(_file)):
                stream.write(f"\t{row}")
            
            for row in open(HTML.format("footer")):
                stream.write(row)
    return False

# Build the whole site, this performs the directory checks,
# generate the piece of HTML blocks form 'pages' dir,
# lastly it sticks together the pages with the templates
def build_site():
    # Directory check and build
    print("Checking directories...")
    error = check_dirs()

    # Batch process
    if error:
        print("Please, set up your files before building the site!")
        return
    else:
        print("Building temporary files...")
        build()
        print("Building site...")
        error = compile()
        if error:
            print("There were some errors...")
        else:
            print("Site built successfully, check the 'dist' folder")

build_site()