from typing import Iterable

# Build each page in a temporary folder, it is called in 'routes' script
def build_content(pages: Iterable[str], content: Iterable[str]):
    for i in range(len(pages)):
        with open(f"build/{pages[i]}.html", 'w') as document:
            document.writelines(content[i])