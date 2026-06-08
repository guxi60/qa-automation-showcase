"""SPA-aware static server for Allure report.
Python's built-in http.server doesn't support HTML5 History API routing.
This script serves the allure-report directory and falls back to index.html
for any path that doesn't correspond to a real file."""

import http.server
import socketserver
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allure-report")


class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPORT_DIR, **kwargs)

    def do_GET(self):
        # If the requested path exists as a file, serve it
        file_path = os.path.join(REPORT_DIR, self.path.lstrip("/"))
        if os.path.isfile(file_path):
            super().do_GET()
            return
        # If the path has a file extension, it's a missing asset — return 404
        if os.path.splitext(self.path)[1]:
            self.send_error(404)
            return
        # Otherwise, serve index.html for SPA routing
        self.path = "/index.html"
        super().do_GET()


if __name__ == "__main__":
    print(f"Serving Allure report at http://localhost:{PORT}")
    print(f"Report directory: {REPORT_DIR}")
    print("Press Ctrl+C to stop.")
    with socketserver.TCPServer(("", PORT), SPAHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
