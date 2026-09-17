#!/usr/bin/env python3
"""
scripts/dev_server.py — Local development server with cleanUrls support.
Mimics Vercel / Caddy production cleanUrls routing:
  /about -> /about.html
  /services -> /services.html
  /blog/posts/slug -> /blog/posts/slug.html
"""

import os
import sys
import http.server
import socketserver

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class CleanUrlHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        # Clean query string
        clean_path = self.path.split('?')[0].split('#')[0]

        # If requesting /blog/posts or /posts, redirect to /blog
        if clean_path.rstrip('/') in ('/blog/posts', '/posts'):
            self.send_response(301)
            self.send_header('Location', '/blog')
            self.end_headers()
            return

        # If requesting a path without extension that matches an .html file
        if clean_path != "/" and not os.path.splitext(clean_path)[1]:
            rel_path = clean_path.lstrip('/')
            # Check direct .html
            html_candidate = os.path.join(ROOT, rel_path + ".html")
            if os.path.isfile(html_candidate):
                # Preserve query string
                query = self.path[len(clean_path):]
                self.path = "/" + rel_path.replace('\\', '/') + ".html" + query
            # Check directory index.html
            elif os.path.isdir(os.path.join(ROOT, rel_path)):
                index_candidate = os.path.join(ROOT, rel_path, "index.html")
                if os.path.isfile(index_candidate):
                    query = self.path[len(clean_path):]
                    self.path = "/" + rel_path.replace('\\', '/') + "/index.html" + query

        return super().do_GET()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CleanUrlHandler) as httpd:
        print("==================================================")
        print(f"[*] Marian Stancik Dev Server running at:")
        print(f"    http://localhost:{PORT}")
        print(f"    Clean URLs enabled (/about -> /about.html)")
        print("==================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
