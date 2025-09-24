#!/usr/bin/env python3
"""
Simple HTTP server to serve static files for PWA functionality
This runs alongside Streamlit to serve the manifest and service worker files
"""

import http.server
import socketserver
import threading
import os
from pathlib import Path

class PWAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/static/'):
            # Serve files from static directory
            file_path = self.path[1:]  # Remove leading /
            if os.path.exists(file_path):
                if file_path.endswith('.json'):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                elif file_path.endswith('.js'):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/javascript')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                elif file_path.endswith('.png'):
                    self.send_response(200)
                    self.send_header('Content-type', 'image/png')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
        
        # Return 404 for other requests
        self.send_error(404, "File not found")

def start_static_server(port=8080):
    """Start the static file server in a separate thread"""
    with socketserver.TCPServer(("", port), PWAHandler) as httpd:
        print(f"Static file server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start static server in background thread
    server_thread = threading.Thread(target=start_static_server, args=(8080,), daemon=True)
    server_thread.start()
    
    # Keep the script running
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down static server")