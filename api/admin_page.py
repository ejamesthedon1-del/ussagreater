from http.server import BaseHTTPRequestHandler
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.admin import create_admin_page


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve admin page"""
        try:
            html = create_admin_page()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Error</h1><p>{str(e)}</p>".encode())

