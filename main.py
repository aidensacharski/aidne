from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import base64
import os

USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "password")
CREDENTIALS = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Authentication
        auth_header = self.headers.get("Authorization")
        if auth_header != f"Basic {CREDENTIALS}":
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Proxy"')
            self.end_headers()
            return

        # Homepage with search bar
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
                <html>
                    <head><title>Proxy Search</title></head>
                    <body>
                        <h1>Welcome to the HTTP Proxy</h1>
                        <form method="get" action="/search">
                            <input type="text" name="q" placeholder="https://example.com" size="50"/>
                            <input type="submit" value="Go"/>
                        </form>
                        <p>This proxy requires basic authentication to access web content.</p>
                    </body>
                </html>
            """
            self.wfile.write(html.encode("utf-8"))
            return

        # Handle search query
        if self.path.startswith("/search"):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query).get("q", [""])[0]

            if not query.startswith("http"):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid URL")
                return

            try:
                with urllib.request.urlopen(query) as response:
                    content = response.read()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Proxy error: {e}".encode("utf-8"))
            return

        # Default: proxy raw URL from /http://... or /https://...
        if self.path.startswith("/http"):
            url = self.path[1:]  # strip the leading slash
            try:
                with urllib.request.urlopen(url) as response:
                    content = response.read()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Proxy error: {e}".encode("utf-8"))
            return

        # Otherwise
        self.send_response(404)
        self.end_headers()

# Run server
if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, ProxyHandler)
    print("Proxy running on http://localhost:8080")
    httpd.serve_forever()