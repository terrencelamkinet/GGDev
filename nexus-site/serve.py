#!/usr/bin/env python3
"""Static file server for NEXUS CRM public website — no-cache for CSS."""
import http.server
import socketserver
import os
import mimetypes
import urllib.parse

PORT = 3100
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexus-site")

os.chdir(DIR)

class NoCacheCSSHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Quiet logging

    def send_head(self):
        path = self.translate_path(self.path)
        # Get the base Content-Type from the super
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            return self.send_error(404, "Not found")
        fs = os.fstat(f.fileno())
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        # Disable caching for CSS, HTML, and JS
        clean_path = self.path.split("?")[0]
        if clean_path.endswith(".css"):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        elif clean_path.endswith((".html", ".js")):
            self.send_header("Cache-Control", "no-cache, must-revalidate")
        self.end_headers()
        return f

with socketserver.TCPServer(("", PORT), NoCacheCSSHandler) as httpd:
    print(f"NEXUS CRM site serving on http://0.0.0.0:{PORT}")
    httpd.serve_forever()
