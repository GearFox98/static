#!/usr/bin/env python3
import os
import shutil
import importlib.util
import sys
import inspect

from static_lib.stutils import prettify_html

# Configuration
PAGES_DIR = "pages"
HTML_DIR = "html"
TEMPLATE_FILE = os.path.join(HTML_DIR, "template.html")
DATA_DIR = "data"
DIST_DIR = "dist"
PLACEHOLDER = "{{CONTENT}}"

def ensure_dirs():
    """Check that required directories exist.
    Returns True if there is an error, False if everything is fine."""
    required = [PAGES_DIR, HTML_DIR]
    for d in required:
        if not os.path.exists(d):
            print(f"Error: Required folder '{d}' does not exist.")
            return True
    # Check that template.html exists
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: Template file '{TEMPLATE_FILE}' not found.")
        return True
    os.makedirs(DIST_DIR, exist_ok=True)
    return False

# Alias for compatibility with the main script
check_dirs = ensure_dirs

def load_module(module_path):
    """Load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec) # type: ignore
    spec.loader.exec_module(module) # type: ignore
    return module

def discover_pages():
    """Find all pages in PAGES_DIR and its subfolders.
    Returns a list of (module_path, relative_path_without_extension)."""
    pages = []
    base_len = len(PAGES_DIR) + 1  # length of "pages/"
    for root, _, files in os.walk(PAGES_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                full_path = os.path.join(root, file)
                # Relative path without extension (e.g., "blog/post1")
                rel_path = full_path[base_len:-3]
                pages.append((full_path, rel_path))
    return pages

def load_template():
    """Read template.html and return its content."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def load_context():
    """Load context from config.py and data/site.json."""
    context = {}
    # Load config.py if it exists
    config_path = os.path.join(os.path.dirname(__file__), "config.py")
    if os.path.exists(config_path):
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec) # type: ignore
        spec.loader.exec_module(config_module) # type: ignore
        for key in dir(config_module):
            if key.isupper():  # Only uppercase variables
                context[key] = getattr(config_module, key)

    # Load data/site.json if it exists
    site_json = os.path.join(DATA_DIR, "site.json")
    if os.path.exists(site_json):
        import json
        with open(site_json, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            context.update(json_data)

    # Add utility functions (example: function to read files from data/)
    def read_data_file(relative_path):
        full_path = os.path.join(DATA_DIR, relative_path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    context['read_data_file'] = read_data_file
    return context

def render_page(module_path, rel_path, context, template):
    """Generate the final HTML for a page and save it in dist/."""
    module = load_module(module_path)
    if not hasattr(module, "render"):
        print(f"Warning: {module_path} has no render() function. Skipping. ⚠️")
        return

    # Call render with or without context depending on its signature
    sig = inspect.signature(module.render)
    if len(sig.parameters) > 0:
        page_content = module.render(context)
    else:
        page_content = module.render()

    # Replace placeholder in the template
    full_html = template.replace(PLACEHOLDER, page_content)

    # Pretty-print the HTML
    full_html = prettify_html(full_html)

    # Determine output path (e.g., "about" -> "dist/about.html")
    output_file = os.path.join(DIST_DIR, rel_path + ".html")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Generated: {output_file} ✔️")

def copy_static():
    """Copy DATA_DIR to DIST_DIR/data."""
    src = DATA_DIR
    dst = os.path.join(DIST_DIR, "data")
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"Static files copied to {dst} ✔️")

def clean_dist():
    """Clean the dist folder."""
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)

def site_build():
    """Main build process. Returns True on success, False on error."""
    try:
        print("Checking directories... 📂")
        if ensure_dirs():
            return False

        print("Cleaning dist... ♻️")
        clean_dist()

        print("Loading template... 📋")
        template = load_template()

        print("Loading context... 🧰")
        context = load_context()

        print("Discovering pages... 🔍")
        pages = discover_pages()
        if not pages:
            print("No pages found in 'pages/'. ⚠️")
            return False

        print(f"Generating {len(pages)} pages... ⚡")
        for module_path, rel_path in pages:
            render_page(module_path, rel_path, context, template)

        print("Copying static files... 📁")
        copy_static()

        print("Site built successfully! 🎉")
        return True
    except Exception as e:
        print(f"Error during build: {e} ❌")
        return False

if __name__ == "__main__":
    success = site_build()
    sys.exit(0 if success else 1)