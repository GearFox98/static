#!/usr/bin/env python3
import os
import shutil
import importlib.util
import sys
import inspect
from lxml import etree, html

# Configuración
PAGES_DIR = "pages"
HTML_DIR = "html"
TEMPLATE_FILE = os.path.join(HTML_DIR, "template.html")
DATA_DIR = "data"
DIST_DIR = "dist"
PLACEHOLDER = "{{CONTENT}}"

def ensure_dirs():
    """Verifica que existan los directorios obligatorios.
    Devuelve True si hay error, False si todo correcto."""
    required = [PAGES_DIR, HTML_DIR]
    for d in required:
        if not os.path.exists(d):
            print(f"Error: La carpeta obligatoria '{d}' no existe.")
            return True
    # Verificar que exista template.html
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: No se encuentra el archivo de plantilla '{TEMPLATE_FILE}'.")
        return True
    os.makedirs(DIST_DIR, exist_ok=True)
    return False

# Alias para compatibilidad con el script principal
check_dirs = ensure_dirs

def load_module(module_path):
    """Carga un módulo Python desde una ruta de archivo."""
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec) # type: ignore
    spec.loader.exec_module(module) # type: ignore
    return module

def discover_pages():
    """Encuentra todas las páginas en PAGES_DIR y sus subcarpetas.
    Devuelve lista de (ruta_del_modulo, ruta_relativa_sin_extension)."""
    pages = []
    base_len = len(PAGES_DIR) + 1  # longitud de "pages/"
    for root, _, files in os.walk(PAGES_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                full_path = os.path.join(root, file)
                # Ruta relativa sin extensión (ej. "blog/post1")
                rel_path = full_path[base_len:-3]
                pages.append((full_path, rel_path))
    return pages

def prettify_html(content):
    """Embellece el HTML usando lxml."""
    try:
        root = html.fromstring(content)
        return etree.tostring(root, encoding='unicode', pretty_print=True)
    except Exception as e:
        print(f"Error al procesar HTML: {e}")
        return content

def load_template():
    """Lee el archivo template.html y devuelve su contenido."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def load_context():
    """Carga el contexto desde config.py y data/site.json."""
    context = {}
    # Cargar config.py si existe
    config_path = os.path.join(os.path.dirname(__file__), "config.py")
    if os.path.exists(config_path):
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec) # type: ignore
        spec.loader.exec_module(config_module) # type: ignore
        for key in dir(config_module):
            if key.isupper():  # Solo variables en mayúsculas
                context[key] = getattr(config_module, key)

    # Cargar data/site.json si existe
    site_json = os.path.join(DATA_DIR, "site.json")
    if os.path.exists(site_json):
        import json
        with open(site_json, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            context.update(json_data)

    # Añadir utilidades (ejemplo: función para leer archivos desde data/)
    def read_data_file(relative_path):
        full_path = os.path.join(DATA_DIR, relative_path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    context['read_data_file'] = read_data_file
    return context

def render_page(module_path, rel_path, context, template):
    """Genera el HTML final para una página y lo guarda en dist/."""
    module = load_module(module_path)
    if not hasattr(module, "render"):
        print(f"Advertencia: {module_path} no tiene función render(). Se omite.")
        return

    # Llamar a render con o sin contexto según la firma
    sig = inspect.signature(module.render)
    if len(sig.parameters) > 0:
        page_content = module.render(context)
    else:
        page_content = module.render()

    # Reemplazar marcador en la plantilla
    full_html = template.replace(PLACEHOLDER, page_content)

    # Embellecer
    full_html = prettify_html(full_html)

    # Determinar ruta de salida (ej. "about" -> "dist/about.html")
    output_file = os.path.join(DIST_DIR, rel_path + ".html")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Generado: {output_file}")

def copy_static():
    """Copia DATA_DIR a DIST_DIR/data."""
    src = DATA_DIR
    dst = os.path.join(DIST_DIR, "data")
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"Archivos estáticos copiados a {dst}")

def clean_dist():
    """Limpia la carpeta dist."""
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)

def site_build():
    """Proceso principal de construcción. Devuelve True si éxito, False si error."""
    try:
        print("Verificando directorios...")
        if ensure_dirs():
            return False

        print("Limpiando dist...")
        clean_dist()

        print("Cargando plantilla...")
        template = load_template()

        print("Cargando contexto...")
        context = load_context()

        print("Descubriendo páginas...")
        pages = discover_pages()
        if not pages:
            print("No se encontraron páginas en 'pages/'.")
            return False

        print(f"Generando {len(pages)} páginas...")
        for module_path, rel_path in pages:
            render_page(module_path, rel_path, context, template)

        print("Copiando archivos estáticos...")
        copy_static()

        print("¡Sitio construido con éxito!")
        return True
    except Exception as e:
        print(f"Error durante la construcción: {e}")
        return False

if __name__ == "__main__":
    success = site_build()
    sys.exit(0 if success else 1)