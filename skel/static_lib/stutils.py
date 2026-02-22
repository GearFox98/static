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
    
    # Expresión regular para encontrar etiquetas HTML (simplificada)
    # Captura: grupos: 1 = etiqueta completa, 2 = nombre, 3 = atributos, 4 = tipo (cierre, apertura, autocierre)
    tag_pattern = re.compile(r'(<!--.*?-->)|(<(/?)([a-zA-Z0-9]+)([^>]*?)>)', re.DOTALL)
    
    lines = []
    indent_level = 0
    last_end = 0
    
    # Función para agregar texto plano con indentación
    def add_text(text):
        if text.strip():
            lines.append(' ' * (indent_level * indent) + text.strip())
        elif text:  # línea vacía pero con espacios, la omitimos
            pass
    
    # Recorremos el HTML buscando etiquetas
    for match in tag_pattern.finditer(html_content):
        start, end = match.span()
        # Texto antes de la etiqueta
        if start > last_end:
            text = html_content[last_end:start]
            if text.strip():
                add_text(text)
        
        # Procesar la etiqueta
        comment, full_tag, slash, tag_name = match.groups()
        if comment:
            # Es un comentario, lo tratamos como bloque
            lines.append(' ' * (indent_level * indent) + comment.strip())
        else:
            tag_name = tag_name.lower()
            is_close = (slash == '/')
            is_self_close = full_tag.strip().endswith('/>') or tag_name in {'meta', 'link', 'br', 'hr', 'img', 'input'}
            
            if is_close:
                # Etiqueta de cierre: disminuir indentación antes de escribir
                indent_level = max(0, indent_level - 1)
                lines.append(' ' * (indent_level * indent) + full_tag)
            elif is_self_close:
                # Etiqueta autocontenida (ej. <br/>)
                lines.append(' ' * (indent_level * indent) + full_tag)
            else:
                # Etiqueta de apertura
                lines.append(' ' * (indent_level * indent) + full_tag)
                # Si es una etiqueta de bloque, aumentamos indentación
                if tag_name in block_tags:
                    indent_level += 1
        
        last_end = end
    
    # Texto restante después de la última etiqueta
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
