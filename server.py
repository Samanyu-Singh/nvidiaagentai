#!/usr/bin/env python3
"""
Simple HTTP server for LegalLensIQ web interface.
"""

import asyncio
import http.server
import json
import os
import socketserver
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse


# Load environment variables from secrets.env
def load_env_file(file_path):
    """Load environment variables from a .env file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value


# Load environment variables
load_env_file("secrets.env")

# Import the researcher agent
import sys

sys.path.append("code")
from docgen_agent.researcher import ResearcherState, graph


class LegalLensIQHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_POST(self):
        """Handle POST requests for chatbot API."""
        if self.path == "/api/chat":
            self.handle_chat_request()
        else:
            self.send_error(404)

    def handle_chat_request(self):
        """Handle chatbot API requests."""
        try:
            # Get request body
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            # Extract message and document content
            user_message = data.get("message", "")
            document_content = data.get("document_content", "")

            if not user_message or not document_content:
                self.send_error(400, "Missing message or document content")
                return

            # Create the full prompt with document context
            full_prompt = f"""
Document Content:
{document_content}

User Question: {user_message}

Please answer the user's question about this document.
"""

            # Run the researcher agent
            async def get_response():
                try:
                    # Create initial state
                    state = ResearcherState(
                        topic=full_prompt,
                        messages=[{"role": "user", "content": user_message}],
                    )

                    # Run the graph
                    result = await graph.ainvoke(state)

                    # Extract the response
                    if (
                        isinstance(result, dict)
                        and "messages" in result
                        and result["messages"]
                    ):
                        # Find the last AI message
                        for message in reversed(result["messages"]):
                            if (
                                hasattr(message, "content")
                                and hasattr(message, "role")
                                and message.role == "assistant"
                            ):
                                return message.content
                            elif (
                                isinstance(message, dict)
                                and message.get("role") == "assistant"
                                and "content" in message
                            ):
                                return message["content"]
                    elif isinstance(result, dict) and "topic" in result:
                        # If no messages, return the topic as response
                        return result["topic"]

                    return "I'm sorry, I couldn't generate a response. Please try rephrasing your question."

                except Exception as e:
                    print(f"Error in researcher agent: {e}")
                    return f"I encountered an error while processing your request: {str(e)}"

            # Run the async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(get_response())
            finally:
                loop.close()

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response_data = {"response": response, "status": "success"}

            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        except Exception as e:
            print(f"Error handling chat request: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.end_headers()


def main():
    """Start the LegalLensIQ web server."""
    PORT = 8080

    # Change to the directory containing index.html
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Check if index.html exists
    if not os.path.exists("index.html"):
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
            webbrowser.open(f"http://localhost:{PORT}")
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
