#!/usr/bin/env python3
"""Static HTTP server with no-cache headers to prevent Cloudflare/CDN caching."""
import http.server
import os

PORT = 8082
DIR = os.path.expanduser('~/projects/ggdev-repo/focus-bird-dev')

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIR)
    server = http.server.HTTPServer(('0.0.0.0', PORT), NoCacheHTTPRequestHandler)
    print(f'Serving {DIR} on port {PORT} with no-cache headers')
    server.serve_forever()
