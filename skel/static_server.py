#
# THIS SERVER IS INTENDED FOR DEVELOPMENT ONLY
# DON'T USE IT IN PRODUCTION.
# DEFAULT LISTEN PORT: 8001
#

from http.server import HTTPServer, BaseHTTPRequestHandler

import os, sys

ADDRESS = '127.0.0.1'
PORT = 8001

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

class QuietHTTPRequestHandler(StaticHTTPRequestHandler):
    def do_GET(self):
        return super().do_GET()
    
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

def serve(interactive: bool):
    try:
        if interactive:
            httpd = HTTPServer((ADDRESS, PORT), QuietHTTPRequestHandler)
        else:
            httpd = HTTPServer((ADDRESS, PORT), StaticHTTPRequestHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        print("\rServer closed")
        sys.exit(0)

if __name__ == "__main__":
    print(f'''Running web server...
                \rALERT: this is a development server, don't use it for production!
                \r---------------
                \rListening on port {PORT}

                \rOpen your browser in: http://{ADDRESS}:{PORT}
                \rHit CTRL+C to close the server.
            ''')
    serve(False)
