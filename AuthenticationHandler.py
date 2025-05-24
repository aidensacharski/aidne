from http.server import BaseHTTPRequestHandler, HTTPServer
import base64

USERNAME = "admin"
PASSWORD = "password"

class AuthProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if the root path is requested
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

        # Authenticate user
        auth_header = self.headers.get('Authorization')
        if not auth_header or not self.is_authenticated(auth_header):
            self.request_auth()
            return

        # Here you could proxy the request to another server (not implemented)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authenticated access granted. Add proxy logic here.")

    def is_authenticated(self, auth_header):
        try:
            method, encoded = auth_header.split()
            if method != "Basic":
                return False
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":")
            return username == USERNAME and password == PASSWORD
        except Exception:
            return False

    def request_auth(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Proxy Access"')
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"401 Unauthorized: Authentication required")

def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, AuthProxyHandler)
    print("Starting proxy server on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
