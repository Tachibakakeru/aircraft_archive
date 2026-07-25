#!/usr/bin/env python3
"""Dev server: serves files with Cache-Control: no-cache to prevent stale-cache issues."""
import http.server

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # suppress per-request noise

if __name__ == "__main__":
    http.server.test(HandlerClass=NoCacheHandler, port=8000, bind="")
