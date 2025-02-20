# Routes file
# Here will be defined all routes in the static site
# Each page should have the name of its own route,
# else it would lead to a dead end!

from stutils import build_content

# Import each page from 'pages' directory
from pages import (
    index,
    about
)

ROUTES = [
    "index",
    "about"
]

# Call build_content with putting the name of the pages (ROUTES) as first argument
# and the second must be the content of the page generated from their respective functions.
def build():
    build_content(
        ROUTES,
        [
            index.get(),
            about.get()
        ]
    )