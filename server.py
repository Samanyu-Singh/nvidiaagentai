#!/usr/bin/env python3
"""
Simple HTTP server for LegalLensIQ web interface.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class LegalLensIQHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the LegalLensIQ web server."""
    PORT = 8000
    
    # Change to the directory containing index.html
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if index.html exists
    if not os.path.exists('index.html'):
        print("❌ Error: index.html not found!")
        print("Please make sure index.html is in the same directory as server.py")
        return
    
    with socketserver.TCPServer(("", PORT), LegalLensIQHandler) as httpd:
        print("🚀 LegalLensIQ Web Server")
        print("=" * 50)
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print("📱 Open your browser and navigate to the URL above")
        print("🔄 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("✅ Browser opened automatically!")
        except:
            print("⚠️ Please open your browser manually")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main() 