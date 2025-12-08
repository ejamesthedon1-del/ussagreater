from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flow_control.store import get_all_login_flows


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Get all login flow overrides"""
        try:
            overrides = get_all_login_flows()
            formatted_overrides = []
            for override in overrides:
                formatted_overrides.append({
                    "user_id": override["user_id"],
                    "forced_route": override["forced_route"],
                    "expires_at": override["expires_at"].isoformat() if override["expires_at"] else None,
                    "updated_at": override["updated_at"].isoformat(),
                    "updated_by": override["updated_by"]
                })
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"overrides": formatted_overrides}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

