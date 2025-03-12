#
# THIS SERVER IS INTENDED FOR DEVELOPMENT ONLY
# DON'T USE IT IN PRODUCTION.
# DEFAULT LISTEN PORT: 8001
#

from http.server import (
    ThreadingHTTPServer,
    BaseHTTPRequestHandler
)
import os, sys

ADDRESS = '127.0.0.1'
PORT = 8001

def get_not_found():
        if os.path.exists("dist/404.html"):
            return "/dist/404.html"
        else:
            return "File not found"

class root(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/dist/index.html'
        else:
            self.path = f'/dist{self.path}'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = get_not_found()
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

def serve():
    try:
        print(f'''Running web server...
            \rALERT: this is a development server, don't use it for production!
            \r---------------
            \rListening on port {PORT}

            \rOpen your browser in: http://{ADDRESS}.{PORT}
            \rHit CTRL+C to close the server.
        ''')
        httpd = ThreadingHTTPServer((ADDRESS, PORT), root)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\rShutting down the server...")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    serve()