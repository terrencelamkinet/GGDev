#!/usr/bin/env python3
"""HTTP server with no-cache headers for exam center."""
import http.server
import socketserver
import socket

PORT = 7872

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

with socketserver.TCPServer(("", PORT), NoCacheHandler, bind_and_activate=False) as httpd:
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    print(f"Serving exam center on port {PORT} (no-cache)")
    httpd.serve_forever()
