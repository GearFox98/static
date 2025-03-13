#
# THIS SERVER IS INTENDED FOR DEVELOPMENT ONLY
# DON'T USE IT IN PRODUCTION.
# DEFAULT LISTEN PORT: 8001
#

from http.server import (
    HTTPServer
)

import sys
from stutils import StaticHTTPRequestHandler

ADDRESS = '127.0.0.1'
PORT = 8001

def serve():
    try:
        httpd = HTTPServer((ADDRESS, PORT), StaticHTTPRequestHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        print("\rServer closed")
        sys.exit(0)

if __name__ == "__main__":
    serve()
