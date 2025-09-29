#!/usr/bin/env python3
"""
Simple HTTP server for DJI360Converter web interface
"""

import http.server
import socketserver
import webbrowser
import argparse
from pathlib import Path
import threading
import time

class DJIConverterHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=Path(__file__).parent, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser(url, delay=1.5):
    """Open browser after a short delay"""
    time.sleep(delay)
    webbrowser.open(url)

def main():
    parser = argparse.ArgumentParser(description='DJI360Converter Web Server')
    parser.add_argument('-p', '--port', type=int, default=8000,
                       help='Port to run server on (default: 8000)')
    parser.add_argument('--no-browser', action='store_true',
                       help='Don\'t automatically open browser')
    
    args = parser.parse_args()
    
    port = args.port
    
    # Create server
    handler = DJIConverterHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            server_url = f"http://localhost:{port}"
            print(f"DJI360Converter server running at {server_url}")
            print("Press Ctrl+C to stop the server")
            
            # Open browser in a separate thread if requested
            if not args.no_browser:
                browser_thread = threading.Thread(target=open_browser, args=(server_url,))
                browser_thread.daemon = True
                browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Error: Port {port} is already in use. Try a different port with -p")
        else:
            print(f"Error starting server: {e}")

if __name__ == '__main__':
    main()