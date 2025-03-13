import os, shutil, time
from typing import Iterable
from http.server import BaseHTTPRequestHandler

# region path
def exists(path: str) -> bool:
    return os.path.exists(path)

# Build each page in a temporary folder, it is called in 'routes' script
def build_content(pages: Iterable[str], content: Iterable[str]):
    for i in range(len(pages)):
        with open(f"build/{pages[i]}.html", 'w') as document:
            document.writelines(content[i])

# Media refactor
def media(res: str):
    return f"\"data/{res}\""

# Clear paths
def clear(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
# endregion

# region server_related
class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/dist/index.html'
        else:
            self.path = f'/dist{self.path}'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            if os.path.exists("dist/404.html"):
                file_to_open = open("dist/404.html").read()
            else:
                file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
    
    def log_message(self, format, *args):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        with open("logs/debug-server.log", 'a') as stream:
            message = format % args
            stream.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          message.translate(self._control_char_table)))
        return

def print_shutdown():
    print("\rShutting down.", end="")
    time.sleep(0.2)
    print("\rShutting down..", end="")
    time.sleep(0.2)
    print("\rShutting down...", end="")
    time.sleep(0.2)

# endregion