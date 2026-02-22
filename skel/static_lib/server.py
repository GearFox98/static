#!/usr/bin/env python3
import os
import threading
import time
import io
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from static_lib import registry
import builder

ADDRESS = "127.0.0.1"
PORT = 8000

_reload_event = threading.Event()


class AutoReloadHandler(SimpleHTTPRequestHandler):
    """HTTP handler with live-reload script injection and /reload endpoint."""

    def do_GET(self):
        if self.path == '/reload':
            self._handle_reload()
            return
        super().do_GET()

    def _handle_reload(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        # Long-poll: wait for rebuild event (up to 30 seconds)
        _reload_event.wait(timeout=30)
        _reload_event.clear()
        self.wfile.write(b'reload')

    def send_head(self):
        """Serve HTML files with injected reload script."""
        path = self.translate_path(self.path)

        # Directory index handling
        if os.path.isdir(path):
            for index in ('index.html', 'index.htm'):
                index_path = os.path.join(path, index)
                if os.path.exists(index_path):
                    path = index_path
                    break

        # Inject script into HTML files
        if path.endswith('.html') and os.path.isfile(path):
            with open(path, 'rb') as f:
                content = f.read()
            script = b'''
                <script>
                    (function listenForReload() {
                        fetch('/reload')
                            .then(() => location.reload())
                            .catch(() => setTimeout(listenForReload, 1000));
                    })();
                </script>
            '''
            modified = content.replace(b'</body>', script + b'</body>')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(modified)))
            self.end_headers()
            return io.BytesIO(modified)

        # For non-HTML files, use base class method
        return super().send_head()


class SimpleHandler(SimpleHTTPRequestHandler):
    """Handler without auto-reload script (for interactive mode)."""
    pass


def print_server(addr, port):
    print(f"⚡ Serving 'dist' directory at http://{addr}:{port}")


def serve(auto_reload=False):
    """
    Start HTTP server serving the 'dist' directory.
    If auto_reload=True, use AutoReloadHandler and start a watcher thread.
    Otherwise use SimpleHandler.
    """
    handler_class = partial(AutoReloadHandler, directory="dist") if auto_reload else partial(SimpleHandler, directory="dist")
    # Use ThreadingHTTPServer to handle requests concurrently
    server = ThreadingHTTPServer((ADDRESS, PORT), handler_class)
    print_server(ADDRESS, PORT)

    if auto_reload:
        watcher = threading.Thread(target=_watch_and_rebuild, daemon=True)
        watcher.start()
        print("Watching for changes... (auto-reload enabled)")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


def _watch_and_rebuild():
    """Background thread: monitor file changes, rebuild, and notify browsers."""
    tstamp = registry.Timestamp(".")
    tstamp.update_times()
    while True:
        if tstamp.compare_times():
            print("Change detected. Rebuilding... 🛠️")
            success = builder.site_build()
            if success:
                print("Rebuild complete. Notifying browsers... 🌐")
                _reload_event.set()
                time.sleep(0.5)  # Brief pause for browsers to reconnect
            tstamp.update_times()
        time.sleep(2)  # Check every 2 seconds to reduce CPU usage