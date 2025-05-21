import http.server
import socketserver
import base64
import urllib.request
import urllib.error
from urllib.parse import urlparse
import os
import threading

PORT = int(os.environ.get("PORT", 8080))
USERNAME = os.environ.get("PROXY_USERNAME", "admin")
PASSWORD = os.environ.get("PROXY_PASSWORD", "password")

class ProxyHandler(http.server.BaseHTTPRequestHandler):

    def authenticate(self):
        auth_header = self.headers.get("Proxy-Authorization")
        if auth_header is None or not auth_header.startswith("Basic "):
            self.send_response(407)
            self.send_header("Proxy-Authenticate", "Basic realm=\"Proxy\"")
            self.end_headers()
            return False

        try:
            encoded = auth_header.split(" ", 1)[1].strip()
            decoded = base64.b64decode(encoded).decode()
            username, password = decoded.split(":", 1)
            if username != USERNAME or password != PASSWORD:
                self.send_response(403)
                self.end_headers()
                return False
        except Exception:
            self.send_response(400, "Bad Request: Invalid Authentication Header")
            self.end_headers()
            return False

        return True

    def do_GET(self):
        if self.path == "/":
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    html = """
        <html>
        <head><title>Proxy Home</title></head>
        <body>
            <h1>Welcome to the HTTP Proxy</h1>
            <p>This proxy requires basic authentication to access web content.</p>
        </body>
        </html>
    """
    self.wfile.write(html.encode("utf-8"))
    return

        parsed_url = urlparse(self.path)
        if not parsed_url.scheme:
            self.send_error(400, "Bad Request: URL must include scheme (http://)")
            return

        try:
            req_headers = {k: v for k, v in self.headers.items() if k.lower() != 'proxy-authorization'}
            req = urllib.request.Request(self.path, headers=req_headers)
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header, value in response.getheaders():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())

        except urllib.error.HTTPError as e:
            self.send_error(e.code, e.reason)
        except urllib.error.URLError as e:
            self.send_error(502, f"Bad Gateway: {e.reason}")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def log_message(self, format, *args):
        pass

class ThreadingSimpleServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == '__main__':
    try:
        server = ThreadingSimpleServer(("0.0.0.0", PORT), ProxyHandler)
        print(f"HTTP proxy server running on port {PORT}")
        threading.Thread(target=server.serve_forever).start()
    except KeyboardInterrupt:
        print("\nProxy server shutting down.")
    except Exception as e:
        print(f"Failed to start server: {e}")
