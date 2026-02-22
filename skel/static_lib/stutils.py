import os, shutil, time, re
from typing import Iterable

# region path
def exists(path: str) -> bool:
    return os.path.exists(path)

def is_empty(path: str) -> bool:
    return False if len(os.listdir(path)) == 0 else True

# Clear paths
def clear(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

# Build each page in a temporary folder, it is called in 'routes' script
def join(pages: Iterable[str], content: Iterable[str]):
    for i in range(len(pages)): # type: ignore
        with open(f"build/{pages[i]}.html", 'w') as document: # type: ignore
            document.writelines(content[i]) # type: ignore

# endregion

# region Prettify

def prettify_html(html_content, indent=2):
    """   
    Args:
        html_content (str): HTML code to format.
        indent (int): Number of spaces to indent.
    
    Returns:
        str: HTML formatted with indentation.
    """
    # Block type tags
    block_tags = {
        'html', 'head', 'body', 'div', 'section', 'article', 'nav', 'aside',
        'header', 'footer', 'main', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'form', 'fieldset',
        'legend', 'details', 'summary', 'figure', 'figcaption', 'pre',
        'blockquote', 'hr', 'br', 'meta', 'link', 'script', 'style'
    }
    # Inline type tags
    inline_tags = {
        'span', 'a', 'b', 'i', 'strong', 'em', 'code', 'img', 'input',
        'button', 'label', 'select', 'option', 'textarea'
    }
    
    # Regular expression to find HTML tags (simplified)
    # Captures: groups: 1 = complete tag, 2 = name, 3 = attributes, 4 = type (closing, opening, self-closing)
    tag_pattern = re.compile(r'(<!--.*?-->)|(<(/?)([a-zA-Z0-9]+)([^>]*?)>)', re.DOTALL)
    
    lines = []
    indent_level = 0
    pos = 0
    last_end = 0
    
    # Function to add plain text with indentation
    def add_text(text):
        if text.strip():
            lines.append(' ' * (indent_level * indent) + text.strip())
        elif text:  # empty line with spaces, we omit it
            pass
    
    # Walk through HTML looking for tags
    for match in tag_pattern.finditer(html_content):
        start, end = match.span()
        # Text before the tag
        if start > last_end:
            text = html_content[last_end:start]
            if text.strip():
                add_text(text)
        
        # Process the tag
        comment, full_tag, slash, tag_name, attrs = match.groups()
        if comment:
            # It's a comment, treat as block
            lines.append(' ' * (indent_level * indent) + comment.strip())
        else:
            tag_name = tag_name.lower()
            is_close = (slash == '/')
            is_self_close = full_tag.strip().endswith('/>') or tag_name in {'meta', 'link', 'br', 'hr', 'img', 'input'}
            
            if is_close:
                # Closing tag: decrease indentation before writing
                indent_level = max(0, indent_level - 1)
                lines.append(' ' * (indent_level * indent) + full_tag)
            elif is_self_close:
                # Self-closing tag (e.g., <br/>)
                lines.append(' ' * (indent_level * indent) + full_tag)
            else:
                # Opening tag
                lines.append(' ' * (indent_level * indent) + full_tag)
                # If it's a block tag, increase indentation
                if tag_name in block_tags:
                    indent_level += 1
        
        last_end = end
    
    # Remaining text after the last tag
    if last_end < len(html_content):
        text = html_content[last_end:]
        if text.strip():
            add_text(text)
    
    return '\n'.join(lines)

# endregion

def print_shutdown():
    print("\rShutting down.", end="")
    time.sleep(0.2)
    print("\rShutting down..", end="")
    time.sleep(0.2)
    print("\rShutting down...", end="")
    time.sleep(0.2)